# %%
import json
import os

from google.cloud import bigquery, storage
from google.oauth2 import service_account


# %%
DATA_FOLDER = "data"
BUSINESS_DOMAIN = "greenery"
location = "asia-southeast1"

# %%
# keyfile = os.environ.get("KEYFILE_PATH")
keyfile = "deb-2023-eb731094ca12-bq&gcs.json"
service_account_info = json.load(open(keyfile))
credentials = service_account.Credentials.from_service_account_info(service_account_info)
project_id = "deb-2023"

# %%
# Load data from Local to GCS
bucket_name = "deb-bootcamp-100018"
storage_client = storage.Client(
    project=project_id,
    credentials=credentials,
)
bucket = storage_client.bucket(bucket_name)

# %%
def load_data_without_partition(data):
    file_path = f"{DATA_FOLDER}/{data}.csv"
    destination_blob_name = f"{BUSINESS_DOMAIN}/{data}/{data}.csv"
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(file_path)

# Load data from GCS to BigQuery
    bigquery_client = bigquery.Client(
        project=project_id,
        credentials=credentials,
        location=location,
    )
    table_id = f"{project_id}.deb_bootcamp.{data}"
    job_config = bigquery.LoadJobConfig(
        skip_leading_rows=1,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        source_format=bigquery.SourceFormat.CSV,
        autodetect=True,
    )
    job = bigquery_client.load_table_from_uri(
        f"gs://{bucket_name}/{destination_blob_name}",
        table_id,
        job_config=job_config,
        location=location,
    )
    job.result()

    table = bigquery_client.get_table(table_id)
    print(f"Loaded {table.num_rows} rows and {len(table.schema)} columns to {table_id}")

# %%
data = [
    "addresses",
    "promos",
    "products",
    "order_items",
]
for each in data:
    load_data_without_partition(each)

# %%
def load_data_with_partition(data, dt, clustering_fields=[]):
    file_path = f"{DATA_FOLDER}/{data}.csv"
    destination_blob_name = f"{BUSINESS_DOMAIN}/{data}/{dt}/{data}.csv"
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(file_path)

    # Load data from GCS to BigQuery
    bigquery_client = bigquery.Client(
        project=project_id,
        credentials=credentials,
        location=location,
    )

    partition = dt.replace("-", "")
    table_id = f"{project_id}.deb_bootcamp.{data}${partition}"
    if clustering_fields:
        job_config = bigquery.LoadJobConfig(
            skip_leading_rows=1,
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
            source_format=bigquery.SourceFormat.CSV,
            autodetect=True,
            time_partitioning=bigquery.TimePartitioning(
                type_=bigquery.TimePartitioningType.DAY,
                field="created_at",
            ),
            clustering_fields=clustering_fields,
        )
    else:
        job_config = bigquery.LoadJobConfig(
            skip_leading_rows=1,
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
            source_format=bigquery.SourceFormat.CSV,
            autodetect=True,
            time_partitioning=bigquery.TimePartitioning(
                type_=bigquery.TimePartitioningType.DAY,
                field="created_at",
            ),
        )
    job = bigquery_client.load_table_from_uri(
        f"gs://{bucket_name}/{destination_blob_name}",
        table_id,
        job_config=job_config,
        location=location,
    )
    job.result()

    table = bigquery_client.get_table(table_id)
    print(f"Loaded {table.num_rows} rows and {len(table.schema)} columns to {table_id}")

# %%
load_data_with_partition("events", "2021-02-10")
load_data_with_partition("orders", "2021-02-10")
load_data_with_partition("users", "2020-10-23", ["first_name", "last_name"])

# %%



