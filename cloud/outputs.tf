output "bucket_name" {
  description = "GCS bucket name for raw data"
  value       = google_storage_bucket.raw_data.name
}

output "dataset_id" {
  description = "BigQuery dataset ID"
  value       = google_bigquery_dataset.challenge.dataset_id
}

output "table_id" {
  description = "BigQuery table ID (fully qualified)"
  value       = "${google_bigquery_dataset.challenge.dataset_id}.${google_bigquery_table.tweets.table_id}"
}

output "service_account_email" {
  description = "Service account email"
  value       = google_service_account.challenge_sa.email
}

output "cloud_function_name" {
  description = "Cloud Function name"
  value       = google_cloudfunctions2_function.load_to_bq.name
}
