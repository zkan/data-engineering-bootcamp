import csv
import json

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.utils import timezone

import requests
from google.cloud import bigquery, storage
from google.oauth2 import service_account


BUSINESS_DOMAIN = "greenery"
LOCATION = "asia-southeast1"
GCP_PROJECT_ID = "ํYOUR_GCP_PROJECT_ID"
DAGS_FOLDER = "/opt/airflow/dags"
DATA = "promos"


def _extract_data(ds):
    url = f"http://34.87.139.82:8000/{DATA}/"
    response = requests.get(url)
    data = response.json()

    with open(f"{DAGS_FOLDER}/{DATA}-{ds}.csv", "w") as f:
        writer = csv.writer(f)
        header = [
            "promo_id",
            "discount",
            "status",
        ]
        writer.writerow(header)
        for each in data:
            data = [
                each["promo_id"],
                each["discount"],
                each["status"],
            ]
            writer.writerow(data)


def _load_data_to_gcs():
    keyfile_gcs = f"{DAGS_FOLDER}/YOUR_KEY_FILE_PATH"
    service_account_info_gcs = json.load(open(keyfile_gcs))
    credentials_gcs = service_account.Credentials.from_service_account_info(
        service_account_info_gcs
    )

    # Load data from Local to GCS
    bucket_name = "deb-bootcamp-YOUR_STUDENT_ID"
    storage_client = storage.Client(
        project=GCP_PROJECT_ID,
        credentials=credentials_gcs,
    )
    bucket = storage_client.bucket(bucket_name)

    file_path = f"{DAGS_FOLDER}/{DATA}-{ds}.csv"
    destination_blob_name = f"raw/{BUSINESS_DOMAIN}/{DATA}/{ds}/{DATA}.csv"
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(file_path)


def _load_data_from_gcs_to_bigquery():
    keyfile_bigquery = f"{DAGS_FOLDER}/YOUR_KEY_FILE_PATH"
    service_account_info_bigquery = json.load(open(keyfile_bigquery))
    credentials_bigquery = service_account.Credentials.from_service_account_info(
        service_account_info_bigquery
    )

    bigquery_client = bigquery.Client(
        project=GCP_PROJECT_ID,
        credentials=credentials_bigquery,
        location=LOCATION,
    )

    table_id = f"{PROJECT_ID}.deb_bootcamp.{DATA}"
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        source_format=bigquery.SourceFormat.PARQUET,
    )

    bucket_name = "deb-bootcamp-YOUR_STUDENT_ID"
    destination_blob_name = f"cleaned/{BUSINESS_DOMAIN}/{DATA}/{ds}/*.parquet"
    job = bigquery_client.load_table_from_uri(
        f"gs://{bucket_name}/{destination_blob_name}",
        table_id,
        job_config=job_config,
        location=LOCATION,
    )
    job.result()

    table = bigquery_client.get_table(table_id)
    print(f"Loaded {table.num_rows} rows and {len(table.schema)} columns to {table_id}")


default_args = {
    "owner": "airflow",
    "start_date": timezone.datetime(2021, 2, 9),
}
with DAG(
    dag_id="greenery_promos_data_pipeline",
    default_args=default_args,
    schedule="@daily",
    catchup=False,
    tags=["DEB", "Skooldio", "greenery"],
):

    # Extract data from Postgres, API, or SFTP
    extract_data = EmptyOperator(
        task_id="extract_data",
    )

    # Load data to GCS
    load_data_to_gcs = EmptyOperator(
        task_id="load_data_to_gcs",
    )
    
    # Submit a Spark app to transform data
    transform_data = EmptyOperator(
        task_id="transform_data",
    )

    # Load data from GCS to BigQuery
    load_data_from_gcs_to_bigquery = EmptyOperator(
        task_id="load_data_from_gcs_to_bigquery",
    )

    # Task dependencies
    extract_data >> load_data_to_gcs >> transform_data >> load_data_from_gcs_to_bigquery