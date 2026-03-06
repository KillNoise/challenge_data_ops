terraform {
  required_version = ">= 1.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# -----------------------------------------------
# GCS Bucket for raw data
# -----------------------------------------------
resource "google_storage_bucket" "raw_data" {
  name          = "${var.project_id}-challenge-raw-data"
  location      = var.region
  force_destroy = true

  uniform_bucket_level_access = true

  labels = {
    environment = "challenge"
    managed_by  = "terraform"
  }
}

# -----------------------------------------------
# BigQuery Dataset
# -----------------------------------------------
resource "google_bigquery_dataset" "challenge" {
  dataset_id  = var.dataset_id
  location    = var.region
  description = "Dataset for the Data Engineering Challenge - Tweet analysis"

  delete_contents_on_destroy = true

  labels = {
    environment = "challenge"
    managed_by  = "terraform"
  }
}

# -----------------------------------------------
# BigQuery Table (schema auto-detected on load)
# -----------------------------------------------
resource "google_bigquery_table" "tweets" {
  dataset_id          = google_bigquery_dataset.challenge.dataset_id
  table_id            = "tweets"
  description         = "Raw tweet data from farmers-protest-tweets JSON"
  deletion_protection = false

  labels = {
    environment = "challenge"
    managed_by  = "terraform"
  }
}

# -----------------------------------------------
# Service Account with minimal permissions
# -----------------------------------------------
resource "google_service_account" "challenge_sa" {
  account_id   = "challenge-data-ops"
  display_name = "Challenge Data Ops SA"
  description  = "Service account for the data engineering challenge"
}

resource "google_project_iam_member" "sa_bq_data_editor" {
  project = var.project_id
  role    = "roles/bigquery.dataEditor"
  member  = "serviceAccount:${google_service_account.challenge_sa.email}"
}

resource "google_project_iam_member" "sa_bq_job_user" {
  project = var.project_id
  role    = "roles/bigquery.jobUser"
  member  = "serviceAccount:${google_service_account.challenge_sa.email}"
}

resource "google_project_iam_member" "sa_storage_admin" {
  project = var.project_id
  role    = "roles/storage.objectAdmin"
  member  = "serviceAccount:${google_service_account.challenge_sa.email}"
}

# -----------------------------------------------
# Enable APIs for Cloud Functions Gen2
# -----------------------------------------------
resource "google_project_service" "cloudfunctions" {
  service            = "cloudfunctions.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "cloudbuild" {
  service            = "cloudbuild.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "run" {
  service            = "run.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "eventarc" {
  service            = "eventarc.googleapis.com"
  disable_on_destroy = false
}

# -----------------------------------------------
# GCS Bucket for Cloud Function source code
# -----------------------------------------------
resource "google_storage_bucket" "function_source" {
  name          = "${var.project_id}-challenge-function-source"
  location      = var.region
  force_destroy = true

  uniform_bucket_level_access = true
}

resource "google_storage_bucket_object" "function_zip" {
  name   = "function-source-${data.archive_file.function_source.output_md5}.zip"
  bucket = google_storage_bucket.function_source.name
  source = data.archive_file.function_source.output_path
}

data "archive_file" "function_source" {
  type        = "zip"
  source_dir  = "${path.module}/function"
  output_path = "${path.module}/function-source.zip"
}

# -----------------------------------------------
# Cloud Function Gen2 (triggered by GCS upload)
# -----------------------------------------------
resource "google_cloudfunctions2_function" "load_to_bq" {
  name     = "load-tweets-to-bigquery"
  location = var.region

  build_config {
    runtime     = "python312"
    entry_point = "load_to_bigquery"

    source {
      storage_source {
        bucket = google_storage_bucket.function_source.name
        object = google_storage_bucket_object.function_zip.name
      }
    }
  }

  service_config {
    max_instance_count = 1
    available_memory   = "512M"
    timeout_seconds    = 540

    service_account_email = google_service_account.challenge_sa.email
  }

  event_trigger {
    trigger_region = var.region
    event_type     = "google.cloud.storage.object.v1.finalized"

    event_filters {
      attribute = "bucket"
      value     = google_storage_bucket.raw_data.name
    }
  }

  depends_on = [
    google_project_service.cloudfunctions,
    google_project_service.cloudbuild,
    google_project_service.run,
    google_project_service.eventarc,
    google_project_iam_member.sa_bq_data_editor,
    google_project_iam_member.sa_bq_job_user,
    google_project_iam_member.sa_storage_admin,
  ]
}
