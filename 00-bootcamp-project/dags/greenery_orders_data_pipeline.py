from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils import timezone
from google.cloud import bigquery, storage
from google.oauth2 import service_account
import os
import json
import requests
import csv

BUSINESS_DOMAIN = "greenery"
LOCATION = "asia-southeast1"
DAGS_FOLDER = "/opt/airflow/dags"
DATA = "orders"
project_id = "deb-2023"
bucket_name = "deb-bootcamp-100018"

# Import modules regarding GCP service account, BigQuery, and GCS 
# Your code here

def _extract_data(ds):
    # Your code below
    url = f"http://34.87.139.82:8000/{DATA}/?created_at={ds}"
    response = requests.get(url)
    data = response.json()
    with open(f"{DAGS_FOLDER}/{DATA}-{ds}.csv", "w") as f:
        writer = csv.writer(f)
        header = data[0].keys()
        writer.writerow(header)

        for each in data:
            writer.writerow(each.values())

def _get_credentials():
    keyfile = "/opt/airflow/dags/deb-2023-eb731094ca12-bq-gcs.json"
    service_account_info = json.load(open(keyfile))
    credentials = service_account.Credentials.from_service_account_info(service_account_info)
    return credentials

def _load_data_to_gcs(ds):
    # Your code below
    credentials=_get_credentials()
    storage_client = storage.Client(
        project=project_id,
        credentials=credentials,
    )
    bucket = storage_client.bucket(bucket_name)

    # events
    file_path = f"{DAGS_FOLDER}/{DATA}-{ds}.csv"
    destination_blob_name = f"{BUSINESS_DOMAIN}/{DATA}/{ds}/{DATA}.csv"
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(file_path)


def _load_data_from_gcs_to_bigquery(ds):
    # Your code below
    credentials=_get_credentials()
    bigquery_client = bigquery.Client(
        project=project_id,
        credentials=credentials,
        location=LOCATION,
    )
    partition = ds.replace("-","")
    table_id = f"{project_id}.deb_bootcamp.{DATA}${partition}"
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
    destination_blob_name = f"{BUSINESS_DOMAIN}/{DATA}/{ds}/{DATA}.csv"
    job = bigquery_client.load_table_from_uri(
        f"gs://{bucket_name}/{destination_blob_name}",
        table_id,
        job_config=job_config,
        location=LOCATION,
    )
    job.result()

    table = bigquery_client.get_table(table_id)
    print(f"Loaded {table.num_rows} rows and {len(table.schema)} columns to {table_id}")
    # pass


default_args = {
    "owner": "airflow",
		"start_date": timezone.datetime(2023, 5, 1),  # Set an appropriate start date here
}
with DAG(
    dag_id="greenery_orders_data_pipeline",  # Replace xxx with the data name
    default_args=default_args,
    schedule="@daily",  # Set your schedule here
    catchup=False,
    tags=["DEB", "2023", "greenery"],
):

    # Extract data from Postgres, API, or SFTP
    extract_data = PythonOperator(
        task_id="extract_data",
        python_callable=_extract_data,
        # op_kwargs={"ds": "{{ ds }}"},
    )
    
    # Load data to GCS
    load_data_to_gcs = PythonOperator(
        task_id="load_data_to_gcs",
        python_callable=_load_data_to_gcs,
        # op_kwargs={"ds": "{{ ds }}"},
    )

    # Load data from GCS to BigQuery
    load_data_from_gcs_to_bigquery = PythonOperator(
        task_id="load_data_from_gcs_to_bigquery",
        python_callable=_load_data_from_gcs_to_bigquery,
        # op_kwargs={"ds": "{{ ds }}"},
    )

    # Task dependencies
    extract_data >> load_data_to_gcs >> load_data_from_gcs_to_bigquery