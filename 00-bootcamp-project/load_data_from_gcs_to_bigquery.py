import json

from google.cloud import bigquery
from google.oauth2 import service_account


DATA_FOLDER = "data"
BUSINESS_DOMAIN = "greenery"
project_id = "dataengineercafe"
location = "asia-southeast1"
bucket_name = "deb4-bootcamp-00"

# Prepare and Load Credentials to Connect to GCP Services
keyfile_bigquery = "YOUR_KEYFILE_PATH"
service_account_info_bigquery = json.load(open(keyfile_bigquery))
credentials_bigquery = service_account.Credentials.from_service_account_info(
    service_account_info_bigquery
)

# Load data from GCS to BigQuery
bigquery_client = bigquery.Client(
    project=project_id,
    credentials=credentials_bigquery,
    location=location,
)

# --- Data ที่ไม่มี partition

data = "addresses"
source_data_in_gcs = f"gs://{bucket_name}/processed/{BUSINESS_DOMAIN}/{data}/*.parquet"
table_id = f"{project_id}.deb_bootcamp.{data}"
job_config = bigquery.LoadJobConfig(
    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    source_format=bigquery.SourceFormat.PARQUET,
    schema=[
        bigquery.SchemaField("address_id", bigquery.SqlTypeNames.STRING),
        bigquery.SchemaField("address", bigquery.SqlTypeNames.STRING),
        bigquery.SchemaField("zipcode", bigquery.SqlTypeNames.STRING),
        bigquery.SchemaField("state", bigquery.SqlTypeNames.STRING),
        bigquery.SchemaField("country", bigquery.SqlTypeNames.STRING),
    ],
)
job = bigquery_client.load_table_from_uri(
    source_data_in_gcs,
    table_id,
    job_config=job_config,
    location=location,
)
job.result()

table = bigquery_client.get_table(table_id)
print(f"Loaded {table.num_rows} rows and {len(table.schema)} columns to {table_id}")

data = "products"
source_data_in_gcs = f"gs://{bucket_name}/processed/{BUSINESS_DOMAIN}/{data}/*.parquet"
table_id = f"{project_id}.deb_bootcamp.{data}"
job_config = bigquery.LoadJobConfig(
    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    source_format=bigquery.SourceFormat.PARQUET,
    schema=[
        bigquery.SchemaField("product_id", bigquery.SqlTypeNames.STRING),
        bigquery.SchemaField("name", bigquery.SqlTypeNames.STRING),
        bigquery.SchemaField("price", bigquery.SqlTypeNames.FLOAT),
        bigquery.SchemaField("inventory", bigquery.SqlTypeNames.INTEGER),
    ],
)
job = bigquery_client.load_table_from_uri(
    source_data_in_gcs,
    table_id,
    job_config=job_config,
    location=location,
)
job.result()

table = bigquery_client.get_table(table_id)
print(f"Loaded {table.num_rows} rows and {len(table.schema)} columns to {table_id}")

data = "order_items"
source_data_in_gcs = f"gs://{bucket_name}/processed/{BUSINESS_DOMAIN}/{data}/*.parquet"
table_id = f"{project_id}.deb_bootcamp.{data}"
job_config = bigquery.LoadJobConfig(
    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    source_format=bigquery.SourceFormat.PARQUET,
    schema=[
        bigquery.SchemaField("order_id", bigquery.SqlTypeNames.STRING),
        bigquery.SchemaField("product_id", bigquery.SqlTypeNames.STRING),
        bigquery.SchemaField("quantity", bigquery.SqlTypeNames.INTEGER),
    ],
)
job = bigquery_client.load_table_from_uri(
    source_data_in_gcs,
    table_id,
    job_config=job_config,
    location=location,
)
job.result()

table = bigquery_client.get_table(table_id)
print(f"Loaded {table.num_rows} rows and {len(table.schema)} columns to {table_id}")

data = "promos"
source_data_in_gcs = f"gs://{bucket_name}/processed/{BUSINESS_DOMAIN}/{data}/*.parquet"
table_id = f"{project_id}.deb_bootcamp.{data}"
job_config = bigquery.LoadJobConfig(
    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    source_format=bigquery.SourceFormat.PARQUET,
    schema=[
        bigquery.SchemaField("promo_id", bigquery.SqlTypeNames.STRING),
        bigquery.SchemaField("discount", bigquery.SqlTypeNames.INTEGER),
        bigquery.SchemaField("status", bigquery.SqlTypeNames.STRING),
    ],
)
job = bigquery_client.load_table_from_uri(
    source_data_in_gcs,
    table_id,
    job_config=job_config,
    location=location,
)
job.result()

table = bigquery_client.get_table(table_id)
print(f"Loaded {table.num_rows} rows and {len(table.schema)} columns to {table_id}")

# --- Data ที่มี partition

data = "events"
dt = "2021-02-10"
source_data_in_gcs = f"gs://{bucket_name}/processed/{BUSINESS_DOMAIN}/{data}/{dt}/*.parquet"
table_id = f"{project_id}.deb_bootcamp.{data}"
job_config = bigquery.LoadJobConfig(
    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    source_format=bigquery.SourceFormat.PARQUET,
    schema=[
        bigquery.SchemaField("event_id", bigquery.SqlTypeNames.STRING),
        bigquery.SchemaField("session_id", bigquery.SqlTypeNames.STRING),
        bigquery.SchemaField("page_url", bigquery.SqlTypeNames.STRING),
        bigquery.SchemaField("created_at", bigquery.SqlTypeNames.TIMESTAMP),
        bigquery.SchemaField("event_type", bigquery.SqlTypeNames.STRING),
        bigquery.SchemaField("user_id", bigquery.SqlTypeNames.STRING),
        bigquery.SchemaField("order_id", bigquery.SqlTypeNames.STRING),
        bigquery.SchemaField("product_id", bigquery.SqlTypeNames.STRING),
    ],
    time_partitioning=bigquery.TimePartitioning(
        type_=bigquery.TimePartitioningType.DAY,
        field="created_at",
    ),
)

partition = dt.replace("-", "")
table_id = f"{project_id}.deb_bootcamp.{data}${partition}"
job = bigquery_client.load_table_from_uri(
    source_data_in_gcs,
    table_id,
    job_config=job_config,
    location=location,
)
job.result()

table = bigquery_client.get_table(table_id)
print(f"Loaded {table.num_rows} rows and {len(table.schema)} columns to {table_id}")

data = "users"
dt = "2020-10-23"
source_data_in_gcs = f"gs://{bucket_name}/processed/{BUSINESS_DOMAIN}/{data}/{dt}/*.parquet"
table_id = f"{project_id}.deb_bootcamp.{data}"
job_config = bigquery.LoadJobConfig(
    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    source_format=bigquery.SourceFormat.PARQUET,
    schema=[
        bigquery.SchemaField("user_id", bigquery.SqlTypeNames.STRING),
        bigquery.SchemaField("first_name", bigquery.SqlTypeNames.STRING),
        bigquery.SchemaField("last_name", bigquery.SqlTypeNames.STRING),
        bigquery.SchemaField("email", bigquery.SqlTypeNames.STRING),
        bigquery.SchemaField("phone_number", bigquery.SqlTypeNames.STRING),
        bigquery.SchemaField("created_at", bigquery.SqlTypeNames.TIMESTAMP),
        bigquery.SchemaField("updated_at", bigquery.SqlTypeNames.TIMESTAMP),
        bigquery.SchemaField("address_id", bigquery.SqlTypeNames.STRING),
    ],
    time_partitioning=bigquery.TimePartitioning(
        type_=bigquery.TimePartitioningType.DAY,
        field="created_at",
    ),
)

partition = dt.replace("-", "")
table_id = f"{project_id}.deb_bootcamp.{data}${partition}"
job = bigquery_client.load_table_from_uri(
    source_data_in_gcs,
    table_id,
    job_config=job_config,
    location=location,
)
job.result()

table = bigquery_client.get_table(table_id)
print(f"Loaded {table.num_rows} rows and {len(table.schema)} columns to {table_id}")

data = "orders"
dt = "2021-02-10"
source_data_in_gcs = f"gs://{bucket_name}/processed/{BUSINESS_DOMAIN}/{data}/{dt}/*.parquet"
table_id = f"{project_id}.deb_bootcamp.{data}"
job_config = bigquery.LoadJobConfig(
    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    source_format=bigquery.SourceFormat.PARQUET,
    schema=[
        bigquery.SchemaField("order_id", bigquery.SqlTypeNames.STRING),
        bigquery.SchemaField("created_at", bigquery.SqlTypeNames.TIMESTAMP),
        bigquery.SchemaField("order_cost", bigquery.SqlTypeNames.FLOAT),
        bigquery.SchemaField("shipping_cost", bigquery.SqlTypeNames.FLOAT),
        bigquery.SchemaField("order_total", bigquery.SqlTypeNames.FLOAT),
        bigquery.SchemaField("tracking_id", bigquery.SqlTypeNames.STRING),
        bigquery.SchemaField("shipping_service", bigquery.SqlTypeNames.STRING),
        bigquery.SchemaField("estimated_delivery_at", bigquery.SqlTypeNames.TIMESTAMP),
        bigquery.SchemaField("delivered_at", bigquery.SqlTypeNames.TIMESTAMP),
        bigquery.SchemaField("status", bigquery.SqlTypeNames.STRING),
        bigquery.SchemaField("user_id", bigquery.SqlTypeNames.STRING),
        bigquery.SchemaField("promo_id", bigquery.SqlTypeNames.STRING),
        bigquery.SchemaField("address_id", bigquery.SqlTypeNames.STRING),
        
    ],
    time_partitioning=bigquery.TimePartitioning(
        type_=bigquery.TimePartitioningType.DAY,
        field="created_at",
    ),
)

partition = dt.replace("-", "")
table_id = f"{project_id}.deb_bootcamp.{data}${partition}"
job = bigquery_client.load_table_from_uri(
    source_data_in_gcs,
    table_id,
    job_config=job_config,
    location=location,
)
job.result()

table = bigquery_client.get_table(table_id)
print(f"Loaded {table.num_rows} rows and {len(table.schema)} columns to {table_id}")
