import datetime

import pendulum

from airflow import DAG
from airflow.providers.google.cloud.transfers.postgres_to_gcs import PostgresToGCSOperator


# Connection Id: gcp_postgres
# Connection Type: postgres
# Host: Server's IP
# Schema: greenery
# Login: postgres
# Password: password
# Port: 5432
POSTGRES_CONNECTION_ID = "gcp_postgres"

# Connection Id : gcp_connection
# Connection Type : Google Cloud
# Project Id : project_id ที่อยู่ในไฟล์ credentail.json
# Keyfile JSON : copy ข้อมูลในทั้งหมดใน credentail.json 
GCP_CONN_ID = "gcp_connection"

SQL_QUERY = """
    SELECT
        event_id
        , session_id
        , user_id
        , page_url
        , created_at
        , event_type
        , order_id
        , product_id
    FROM public.events where DATE(created_at) = '2021-02-12'
"""
GCS_BUCKET = "example-78147"
FILENAME = "postgres/2021-02-12/events.csv"

with DAG(
    dag_id="example_postgres_to_gcs_operator",
    schedule=None,
    start_date=pendulum.datetime(2023, 4, 15),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=60),
) as dag:

    postgres_to_gcs = PostgresToGCSOperator(
        task_id=f'postgres_to_gcs',
        postgres_conn_id=POSTGRES_CONNECTION_ID,
        sql=SQL_QUERY,
        bucket=GCS_BUCKET,
        filename=FILENAME,
        export_format='avro',
        gzip=False,
        use_server_side_cursor=True,
        gcp_conn_id=GCP_CONN_ID,
    )
