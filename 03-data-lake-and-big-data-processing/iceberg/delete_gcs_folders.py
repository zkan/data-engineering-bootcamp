import json
import os

from google.cloud import storage
from google.oauth2 import service_account


GCP_PROJECT_ID = "dataengineercafe" # Replace with your GCP project ID
GCS_BUCKET = "iceberg-tmp-zkan-123" # Replace with your GCS bucket

keyfile = "dataengineercafe-61ef403fcaf4.json"
service_account_info = json.load(open(keyfile))
credentials = service_account.Credentials.from_service_account_info(service_account_info)
project_id = "dataengineercafe"

storage_client = storage.Client(
    project=project_id,
    credentials=credentials,
)
bucket = storage_client.get_bucket(GCS_BUCKET)

blobs = bucket.list_blobs(prefix="default.db/")

for blob in blobs:
    blob.delete()