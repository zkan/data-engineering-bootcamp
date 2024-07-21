import datetime

import pendulum
from airflow import DAG
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator

# Connection Id : gcp_connection
# Connection Type : Google Cloud
# Project Id : project_id ที่อยู่ในไฟล์ credentail.json
# Keyfile JSON : copy ข้อมูลในทั้งหมดใน credentail.json 
GCP_CONN_ID = "gcp_connection"

GCS_BUCKET = "example-78147"
FILENAME = "postgres/2021-02-12/events.csv"

DATASET_NAME = "greenery"
TABLE_NAME = "events"

with DAG(
    dag_id="example_gcs_to_bigquery_operator",
    schedule=None,
    start_date=pendulum.datetime(2023, 4, 15),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=60),
) as dag:

    gcs_to_bq = GCSToBigQueryOperator(
        task_id="gcs_to_bigquery",
        bucket=GCS_BUCKET,
        source_objects=[FILENAME],
        source_format="csv",
        destination_project_dataset_table=f"{DATASET_NAME}.{TABLE_NAME}$20210212",
        schema_fields=[
            {"name": "event_id", "mode": "NULLABLE", "type": "STRING"},
            {"name": "session_id", "mode": "NULLABLE", "type": "STRING"},
            {"name": "user_id", "mode": "NULLABLE", "type": "STRING"},
            {"name": "page_url", "mode": "NULLABLE", "type": "STRING"},
            {"name": "created_at", "mode": "NULLABLE", "type": "TIMESTAMP"},
            {"name": "event_type", "mode": "NULLABLE", "type": "STRING"},
            {"name": "order_id", "mode": "NULLABLE", "type": "STRING"},
            {"name": "product_id", "mode": "NULLABLE", "type": "STRING"}
        ],
        write_disposition="WRITE_TRUNCATE",
        gcp_conn_id=GCP_CONN_ID,
        time_partitioning={
            "field": "created_at",
            "type": "DAY",
        },
    )
