#!/bin/bash
# -----------------------------------------------------------
# load_data.sh - Upload JSON to GCS and load into BigQuery
#
# Usage:
#   ./load_data.sh <PROJECT_ID> [REGION]
#
# Prerequisites:
#   - gcloud CLI authenticated (gcloud auth login)
#   - Terraform already applied (bucket and table exist)
# -----------------------------------------------------------

set -euo pipefail

PROJECT_ID="${1:?Usage: ./load_data.sh <PROJECT_ID> [REGION]}"
REGION="${2:-us-central1}"
DATASET="challenge_data_ops"
TABLE="tweets"
BUCKET="${PROJECT_ID}-challenge-raw-data"
JSON_FILE="../farmers-protest-tweets-2021-2-4.json"

echo "=== Step 1: Upload JSON to GCS ==="
gsutil -o GSUtil:parallel_composite_upload_threshold=150M \
  cp "${JSON_FILE}" "gs://${BUCKET}/raw/farmers-protest-tweets.json"
echo "Uploaded to gs://${BUCKET}/raw/"

echo ""
echo "=== Step 2: Load into BigQuery ==="
bq load \
  --project_id="${PROJECT_ID}" \
  --source_format=NEWLINE_DELIMITED_JSON \
  --autodetect \
  --replace \
  --max_bad_records=100 \
  "${DATASET}.${TABLE}" \
  "gs://${BUCKET}/raw/farmers-protest-tweets.json"
echo "Loaded into ${PROJECT_ID}:${DATASET}.${TABLE}"

echo ""
echo "=== Step 3: Verify row count ==="
bq query --project_id="${PROJECT_ID}" --use_legacy_sql=false \
  "SELECT COUNT(*) as total_rows FROM \`${PROJECT_ID}.${DATASET}.${TABLE}\`"

echo ""
echo "Data loading complete."
