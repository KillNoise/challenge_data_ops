terraform {
  required_version = ">= 1.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
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
