from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils import timezone
# Import modules regarding GCP service account, BigQuery, and GCS 
from google.cloud import bigquery, storage
from google.oauth2 import service_account
import requests
import csv
import json

BUSINESS_DOMAIN = "greenery"
LOCATION = "asia-southeast1"
PROJECT_ID = "deb-1-by-skooldio"
DAGS_FOLDER = "/opt/airflow/dags"
DATA = "addresses"
def _extract_data(ds):
    url = f"http://34.87.139.82:8000/{DATA}/"
    response = requests.get(url)
    data = response.json()
    with open(f"{DAGS_FOLDER}/{DATA}.csv","w") as f:
        writer = csv.writer(f)
        header = ["address_id","address","zipcode",'state',"country"]
        writer.writerow(header)

        for each in data:
            data = [
                each["address_id"], 
                each["address"],
                each["zipcode"],
                each['state'],
                each['country']
            ]
            writer.writerow(data)

def _load_data_to_gcs(ds):
    keyfile_gcs = "/opt/airflow/dags/deb-1-by-skooldio-93a52cb49694.json"
    service_account_info_gcs = json.load(open(keyfile_gcs))
    credentials_gcs = service_account.Credentials.from_service_account_info(
        service_account_info_gcs
    )
    bucket_name = "deb-bootcamp-100022"
    storage_client = storage.Client(
        project = PROJECT_ID,
        credentials = credentials_gcs
    )
    bucket = storage_client.bucket(bucket_name)

    file_path = f"{DAGS_FOLDER}/{DATA}.csv"
    destination_blob_name = f"{BUSINESS_DOMAIN}/{DATA}/{DATA}.csv"
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(file_path)

def _load_data_from_gcs_to_bigquery():
    keyfile_bigquery = "/opt/airflow/dags/deb-1-by-skooldio-9c5dab1f27c8.json"
    service_account_info_bigquery = json.load(open(keyfile_bigquery))
    credentials_bigquery = service_account.Credentials.from_service_account_info(
        service_account_info_bigquery
    )

    bigquery_client = bigquery.Client(
        project=PROJECT_ID,
        credentials=credentials_bigquery,
        location=LOCATION,
    )

    table_id = f"{PROJECT_ID}.deb_bootcamp.{DATA}"
    job_config = bigquery.LoadJobConfig(
        skip_leading_rows=1,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        source_format=bigquery.SourceFormat.CSV,
        autodetect=True,
    )

    bucket_name = "deb-bootcamp-100022"
    destination_blob_name = f"{BUSINESS_DOMAIN}/{DATA}/{DATA}.csv"
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
		"start_date": timezone.datetime(2021, 2, 9),  # Set an appropriate start date here
}
with DAG(
    dag_id="greenery_addresses_data_pipeline",  # Replace xxx with the data name
    default_args=default_args,
    schedule="@daily",  # Set your schedule here
    catchup=False,
    tags=["DEB", "2023", "greenery"],
):

    # Extract data from Postgres, API, or SFTP
    extract_data = PythonOperator(
        task_id="extract_data",
        python_callable=_extract_data,
        # op_kwargs = {"ds":"{{ ds }}"}
    )

    # Load data to GCS
    load_data_to_gcs = PythonOperator(
        task_id="load_data_to_gcs",
        python_callable=_load_data_to_gcs,
    )

    # Load data from GCS to BigQuery
    load_data_from_gcs_to_bigquery = PythonOperator(
        task_id="load_data_from_gcs_to_bigquery",
        python_callable=_load_data_from_gcs_to_bigquery,
    )

    # Task dependencies
    extract_data >> load_data_to_gcs >> load_data_from_gcs_to_bigquery