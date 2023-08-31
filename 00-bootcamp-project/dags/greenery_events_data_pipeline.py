import csv
import json

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import BranchPythonOperator, PythonOperator
from airflow.utils import timezone

import requests
from google.cloud import bigquery, storage
from google.oauth2 import service_account


BUSINESS_DOMAIN = "greenery"
LOCATION = "asia-southeast1"
PROJECT_ID = "dataengineercafe"
DAGS_FOLDER = "/opt/airflow/dags"
DATA = "events"


def _extract_data(ds):
    url = f"http://34.87.139.82:8000/{DATA}/?created_at={ds}"
    response = requests.get(url)
    data = response.json()

    if data:
        with open(f"{DAGS_FOLDER}/{DATA}-{ds}.csv", "w") as f:
            writer = csv.writer(f)
            header = [
                "event_id",
                "session_id",
                "page_url",
                "created_at",
                "event_type",
                "user",
                "order",
                "product",
            ]
            writer.writerow(header)
            for each in data:
                data = [
                    each["event_id"],
                    each["session_id"],
                    each["page_url"],
                    each["created_at"],
                    each["event_type"],
                    each["user"],
                    each["order"],
                    each["product"]
                ]
                writer.writerow(data)
        return "load_data_to_gcs"
    else:
        return "do_nothing"


def _load_data_to_gcs(ds):
    keyfile_gcs = f"{DAGS_FOLDER}/dataengineercafe-deb2-loading-files-to-gcs-509ec0e91d64.json"
    service_account_info_gcs = json.load(open(keyfile_gcs))
    credentials_gcs = service_account.Credentials.from_service_account_info(
        service_account_info_gcs
    )

    # Load data from Local to GCS
    bucket_name = "deb2-bootcamp-200031999"
    storage_client = storage.Client(
        project=PROJECT_ID,
        credentials=credentials_gcs,
    )
    bucket = storage_client.bucket(bucket_name)

    file_path = f"{DAGS_FOLDER}/{DATA}-{ds}.csv"
    destination_blob_name = f"{BUSINESS_DOMAIN}/{DATA}/{ds}/{DATA}.csv"
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(file_path)


def _load_data_from_gcs_to_bigquery(ds, ds_nodash):
    keyfile_bigquery = f"{DAGS_FOLDER}/dataengineercafe-deb2-gcs-to-bigquery-906983b6ae02.json"
    service_account_info_bigquery = json.load(open(keyfile_bigquery))
    credentials_bigquery = service_account.Credentials.from_service_account_info(
        service_account_info_bigquery
    )

    bigquery_client = bigquery.Client(
        project=PROJECT_ID,
        credentials=credentials_bigquery,
        location=LOCATION,
    )

    table_id = f"{PROJECT_ID}.deb_bootcamp.{DATA}${ds_nodash}"
    job_config = bigquery.LoadJobConfig(
        skip_leading_rows=1,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        source_format=bigquery.SourceFormat.CSV,
        autodetect=True,
    )

    bucket_name = "deb2-bootcamp-200031999"
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


default_args = {
    "owner": "airflow",
    "start_date": timezone.datetime(2021, 2, 9),
}
with DAG(
    dag_id="greenery_events_data_pipeline",
    default_args=default_args,
    schedule="@daily",
    catchup=False,
    tags=["DEB", "2023", "greenery"],
):

    start = EmptyOperator(task_id="start")

    # Extract data from Postgres, API, or SFTP
    extract_data = BranchPythonOperator(
        task_id="extract_data",
        python_callable=_extract_data,
    )

    do_nothing = EmptyOperator(task_id="do_nothing")

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

    end = EmptyOperator(task_id="end", trigger_rule="one_success")

    # Task dependencies
    start >> extract_data >> load_data_to_gcs >> load_data_from_gcs_to_bigquery >> end
    extract_data >> do_nothing >> end