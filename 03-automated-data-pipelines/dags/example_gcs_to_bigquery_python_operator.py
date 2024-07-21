import datetime

import pendulum

from airflow import DAG
from airflow.decorators import task
from airflow.models import Variable

from google.cloud import bigquery
from google.oauth2 import service_account


GCS_BUCKET = "example-78147"
FILENAME = "postgres/2021-02-12/events.csv"

DATASET_NAME = "greenery"
TABLE_NAME = "events"

# สร้าง Variable
# Key : gcp_credential_secret
# Val : copy ข้อมูลในทั้งหมดใน credentail.json
VARIABLE_BIGQUERY_CREDENTIAL = "gcp_credential_secret"

with DAG(
    dag_id="example_gcs_to_bigquery_python_operator",
    schedule=None,
    start_date=pendulum.datetime(2023, 4, 15),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=60),
) as dag:

    @task(task_id="gcs_to_bigquery")
    def load_data_from_gcs_to_bigquery():
        gsutil_uri = f"gs://{GCS_BUCKET}/{FILENAME}"

        bq_credential_secret = Variable.get(VARIABLE_BIGQUERY_CREDENTIAL, deserialize_json=True)
        bq_client = bigquery.Client(
            credentials=service_account.Credentials.from_service_account_info(bq_credential_secret),
        )
        table_id = f"cultivated-list-383715.{DATASET_NAME}.{TABLE_NAME}$20210212"
        bq_table = bq_client.get_table(table_id)

        job_config = bigquery.LoadJobConfig(
            schema=bq_table.schema,
            source_format=bigquery.SourceFormat.CSV,
            write_disposition="WRITE_TRUNCATE",
            skip_leading_rows=1
        )

        load_job = bq_client.load_table_from_uri(
            gsutil_uri, table_id, job_config=job_config
        )
        load_job.result()


    load_data_from_gcs_to_bigquery_task = load_data_from_gcs_to_bigquery()