from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils import timezone
from google.cloud import bigquery, storage
from google.oauth2 import service_account
import pandas as pd
import os
import json
import csv
import requests

BUSINESS_DOMAIN = "greenery"
LOCATION = "asia-southeast1"
PROJECT_ID = "dataengineercafe"
DAGS_FOLDER = "/opt/airflow/dags"
DATA = "promos"
project_id = "deb-2023"
bucket_name = "deb-bootcamp-100018"
header = ["promo_id", "discount", "status"]

# Import modules regarding GCP service account, BigQuery, and GCS 
# Your code here

def _extract_data():
    # Your code below
    pg_hook = PostgresHook(postgres_conn_id="my_postgres_conn", schema="greenery")
    connection = pg_hook.get_conn()
    cursor = connection.cursor()
    sql = """select {} from {}""".format(', '.join(header), DATA)
    cursor.execute(sql)
    rows = cursor.fetchall()
    for each in rows:
        print(each)

def _dump_data(table: str):
    pg_hook = PostgresHook(postgres_conn_id="my_postgres_conn", schema="greenery")
    out_file = f"{DAGS_FOLDER}/{table}"
    pg_hook.bulk_dump(table, out_file)
    return {'out_file': out_file, 'tb_name': table}

def _data_to_csv(pull_task, **kwargs):
    pull_data = kwargs['ti'].xcom_pull(task_ids=pull_task)
    input_file = pull_data['out_file']
    df = pd.read_csv(input_file, delimiter='\t', header=None)
    df.columns = header
    df.to_csv(f'{input_file}.csv', index=None)
    os.remove(input_file)

def _get_credentials():
    keyfile = "/opt/airflow/dags/deb-2023-eb731094ca12-bq-gcs.json"
    service_account_info = json.load(open(keyfile))
    credentials = service_account.Credentials.from_service_account_info(service_account_info)
    return credentials

def _load_data_to_gcs():
    # Your code below
    credentials=_get_credentials()
    storage_client = storage.Client(
        project=project_id,
        credentials=credentials,
    )
    bucket = storage_client.bucket(bucket_name)

    # order_items
    file_path = f"{DAGS_FOLDER}/{DATA}.csv"
    destination_blob_name = f"{BUSINESS_DOMAIN}/{DATA}/{DATA}.csv"
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(file_path)


def _load_data_from_gcs_to_bigquery():
    # Your code below
    credentials=_get_credentials()
    bigquery_client = bigquery.Client(
        project=project_id,
        credentials=credentials,
        location=LOCATION,
    )
    table_id = f"{project_id}.deb_bootcamp.{DATA}"
    job_config = bigquery.LoadJobConfig(
        skip_leading_rows=1,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        source_format=bigquery.SourceFormat.CSV,
        autodetect=True,
    )
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
    # pass


default_args = {
    "owner": "airflow",
		"start_date": timezone.datetime(2023, 5, 1),  # Set an appropriate start date here
}
with DAG(
    dag_id="greenery_promos_data_pipeline",  # Replace xxx with the data name
    default_args=default_args,
    schedule=None,  # Set your schedule here
    catchup=False,
    tags=["DEB", "2023", "greenery"],
):

    # Extract data from Postgres, API, or SFTP
    extract_data = PythonOperator(
        task_id="extract_data",
        python_callable=_extract_data,
    )

    dump_data = PythonOperator(
        task_id="dump_data",
        python_callable=_dump_data,
        op_kwargs={"table": DATA},
    )

    data_to_csv = PythonOperator(
        task_id="data_to_csv",
        python_callable=_data_to_csv,
        op_kwargs={"pull_task": "dump_data"},
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
    extract_data >> dump_data >> data_to_csv >> load_data_to_gcs >> load_data_from_gcs_to_bigquery