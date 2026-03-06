"""
Cloud Function: Auto-load JSON from GCS into BigQuery.

Triggered by GCS object finalize (upload) events.
Only processes files in the raw/ prefix to avoid false triggers.
"""

import functions_framework
from google.cloud import bigquery
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PROJECT_ID = None  # Auto-detected from environment
DATASET_ID = "challenge_data_ops"
TABLE_ID = "tweets"


@functions_framework.cloud_event
def load_to_bigquery(cloud_event):
    """Triggered by GCS object finalize. Loads JSON into BigQuery."""
    data = cloud_event.data

    bucket_name = data["bucket"]
    file_name = data["name"]
    file_size = data.get("size", "unknown")

    logger.info(f"File uploaded: gs://{bucket_name}/{file_name} ({file_size} bytes)")

    # Only process files in raw/ prefix
    if not file_name.startswith("raw/"):
        logger.info(f"Skipping {file_name} -- not in raw/ prefix")
        return

    # Only process JSON files
    if not file_name.endswith(".json"):
        logger.info(f"Skipping {file_name} -- not a JSON file")
        return

    client = bigquery.Client()
    table_ref = f"{client.project}.{DATASET_ID}.{TABLE_ID}"
    uri = f"gs://{bucket_name}/{file_name}"

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        autodetect=True,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        max_bad_records=100,
    )

    logger.info(f"Loading {uri} into {table_ref}")
    load_job = client.load_table_from_uri(uri, table_ref, job_config=job_config)
    load_job.result()  # Wait for completion

    table = client.get_table(table_ref)
    logger.info(f"Load complete: {table.num_rows} rows in {table_ref}")
