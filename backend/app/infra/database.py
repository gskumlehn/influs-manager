import os
from contextlib import contextmanager

from google.cloud import bigquery

PROJECT_ID = os.getenv("GCP_PROJECT_ID", "your-project-id")
DATASET_ID = os.getenv("BIGQUERY_DATASET_ID", "influencer_db")

client = bigquery.Client(project=PROJECT_ID)

@contextmanager
def get_client():
    try:
        yield client
    except Exception:
        raise

def get_table_id(table_name: str) -> str:
    return f"{PROJECT_ID}.{DATASET_ID}.{table_name}"
