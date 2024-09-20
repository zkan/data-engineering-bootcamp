import json

from google.cloud import storage
from google.oauth2 import service_account


DATA_FOLDER = "data"
BUSINESS_DOMAIN = "greenery"
project_id = "dataengineercafe"
location = "asia-southeast1"
bucket_name = "deb4-bootcamp-00"

# Prepare and Load Credentials to Connect to GCP Services
keyfile_gcs = "YOUR_KEYFILE_PATH"
service_account_info_gcs = json.load(open(keyfile_gcs))
credentials_gcs = service_account.Credentials.from_service_account_info(
    service_account_info_gcs
)

# Load data from Local to GCS
storage_client = storage.Client(
    project=project_id,
    credentials=credentials_gcs,
)
bucket = storage_client.bucket(bucket_name)

# --- Data ที่ไม่มี partition

data = "addresses"
file_path = f"{DATA_FOLDER}/{data}.csv"
destination_blob_name = f"raw/{BUSINESS_DOMAIN}/{data}/{data}.csv"
blob = bucket.blob(destination_blob_name)
blob.upload_from_filename(file_path)

data = "products"
file_path = f"{DATA_FOLDER}/{data}.csv"
destination_blob_name = f"raw/{BUSINESS_DOMAIN}/{data}/{data}.csv"
blob = bucket.blob(destination_blob_name)
blob.upload_from_filename(file_path)

data = "order_items"
file_path = f"{DATA_FOLDER}/{data}.csv"
destination_blob_name = f"raw/{BUSINESS_DOMAIN}/{data}/{data}.csv"
blob = bucket.blob(destination_blob_name)
blob.upload_from_filename(file_path)

data = "promos"
file_path = f"{DATA_FOLDER}/{data}.csv"
destination_blob_name = f"raw/{BUSINESS_DOMAIN}/{data}/{data}.csv"
blob = bucket.blob(destination_blob_name)
blob.upload_from_filename(file_path)


# --- Data ที่มี partition

data = "events"
dt = "2021-02-10"
file_path = f"{DATA_FOLDER}/{data}.csv"
destination_blob_name = f"raw/{BUSINESS_DOMAIN}/{data}/{dt}/{data}.csv"
blob = bucket.blob(destination_blob_name)
blob.upload_from_filename(file_path)

data = "users"
dt = "2020-10-23"
file_path = f"{DATA_FOLDER}/{data}.csv"
destination_blob_name = f"raw/{BUSINESS_DOMAIN}/{data}/{dt}/{data}.csv"
blob = bucket.blob(destination_blob_name)
blob.upload_from_filename(file_path)

data = "orders"
dt = "2021-02-10"
file_path = f"{DATA_FOLDER}/{data}.csv"
destination_blob_name = f"raw/{BUSINESS_DOMAIN}/{data}/{dt}/{data}.csv"
blob = bucket.blob(destination_blob_name)
blob.upload_from_filename(file_path)
