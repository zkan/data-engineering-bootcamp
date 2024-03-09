import json
import os

from google.cloud import bigquery, storage
from google.oauth2 import service_account


DATA_FOLDER = "data"
BUSINESS_DOMAIN = "greenery"
LOCATION = "asia-southeast1"
PROJECT_ID = "dataengineercafe"
BUCKET_NAME = "deb3-bootcamp-00"

# Prepare and Load Credentials to Connect to GCP Services
keyfile_gcs = "dataengineercafe-deb3-uploading-files-to-gcs-27c6014869cf.json"
service_account_info_gcs = json.load(open(keyfile_gcs))
credentials_gcs = service_account.Credentials.from_service_account_info(
    service_account_info_gcs
)
keyfile_bigquery = "dataengineercafe-deb3-load-files-to-bigquery-61580246a511.json"
service_account_info_bigquery = json.load(open(keyfile_bigquery))
credentials_bigquery = service_account.Credentials.from_service_account_info(
    service_account_info_bigquery
)

# Prepare clients for GCS and BigQuery
storage_client = storage.Client(
    project=PROJECT_ID,
    credentials=credentials_gcs,
)
bigquery_client = bigquery.Client(
    project=PROJECT_ID,
    credentials=credentials_bigquery,
    location=LOCATION,
)


def load_to_gcs_without_partition(storage_client, data):
    bucket = storage_client.bucket(BUCKET_NAME)
    file_path = f"{DATA_FOLDER}/{data}.csv"
    destination_blob_name = f"{BUSINESS_DOMAIN}/{data}/{data}.csv"
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(file_path)

    return destination_blob_name


def load_to_bigquery_without_partition(bigquery_client, data, destination_blob_name):
    job_config = bigquery.LoadJobConfig(
        skip_leading_rows=1,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        source_format=bigquery.SourceFormat.CSV,
        autodetect=True,
    )

    table_id = f"{PROJECT_ID}.deb_bootcamp.{data}"
    job = bigquery_client.load_table_from_uri(
        f"gs://{BUCKET_NAME}/{destination_blob_name}",
        table_id,
        job_config=job_config,
        location=LOCATION,
    )
    job.result()

    table = bigquery_client.get_table(table_id)
    print(f"Loaded {table.num_rows} rows and {len(table.schema)} columns to {table_id}")

# Addresses
destination_blob_name = load_to_gcs_without_partition(storage_client=storage_client, data="addresses")
load_to_bigquery_without_partition(
    bigquery_client=bigquery_client,
    data="addresses",
    destination_blob_name=destination_blob_name,
)

# Products
destination_blob_name = load_to_gcs_without_partition(storage_client=storage_client, data="products")
load_to_bigquery_without_partition(
    bigquery_client=bigquery_client,
    data="products",
    destination_blob_name=destination_blob_name,
)

# Order Items
destination_blob_name = load_to_gcs_without_partition(storage_client=storage_client, data="order_items")
load_to_bigquery_without_partition(
    bigquery_client=bigquery_client,
    data="order_items",
    destination_blob_name=destination_blob_name,
)

# ---------

def load_to_gcs_with_partition(storage_client, data, dt):
    bucket = storage_client.bucket(BUCKET_NAME)
    file_path = f"{DATA_FOLDER}/{data}.csv"
    destination_blob_name = f"{BUSINESS_DOMAIN}/{data}/{dt}/{data}.csv"
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(file_path)

    return destination_blob_name


def load_to_bigquery_with_partition(bigquery_client, data, destination_blob_name, partitioned_by_field, dt):
    job_config = bigquery.LoadJobConfig(
        skip_leading_rows=1,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        source_format=bigquery.SourceFormat.CSV,
        autodetect=True,
        time_partitioning=bigquery.TimePartitioning(
            type_=bigquery.TimePartitioningType.DAY,
            field=partitioned_by_field,
        ),
    )

    partition = dt.replace("-", "")
    table_id = f"{PROJECT_ID}.deb_bootcamp.{data}${partition}"
    job = bigquery_client.load_table_from_uri(
        f"gs://{BUCKET_NAME}/{destination_blob_name}",
        table_id,
        job_config=job_config,
        location=LOCATION,
    )
    job.result()

    table = bigquery_client.get_table(table_id)
    print(f"Loaded {table.num_rows} rows and {len(table.schema)} columns to {table_id}")


# Events
destination_blob_name = load_to_gcs_with_partition(storage_client=storage_client, data="events", dt="2021-02-10")
load_to_bigquery_with_partition(
    bigquery_client=bigquery_client,
    data="events",
    destination_blob_name=destination_blob_name,
    partitioned_by_field="created_at",
    dt="2021-02-10",
)

# Users
destination_blob_name = load_to_gcs_with_partition(storage_client=storage_client, data="users", dt="2020-10-23")
load_to_bigquery_with_partition(
    bigquery_client=bigquery_client,
    data="users",
    destination_blob_name=destination_blob_name,
    partitioned_by_field="created_at",
    dt="2020-10-23",
)

# Orders
destination_blob_name = load_to_gcs_with_partition(storage_client=storage_client, data="orders", dt="2021-02-10")
load_to_bigquery_with_partition(
    bigquery_client=bigquery_client,
    data="orders",
    destination_blob_name=destination_blob_name,
    partitioned_by_field="created_at",
    dt="2021-02-10",
)
