
from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.utils import timezone


"""
#### Connection

Connection Id: my_spark
Connection Type: Spark,
Host: spark://spark-master
Port: 7077
Deploy mode: client
Spark binary: spark-submit
"""

with DAG(
    dag_id="example_spark_operator",
    schedule_interval=None,
    start_date=timezone.datetime(2024, 7, 30),
    catchup=False,
    tags=["spark"],
):

    submit_demo_app = SparkSubmitOperator(
        task_id="submit_demo_app",
        application="/opt/airflow/dags/demo.py",
        conn_id="my_spark",
    )

    submit_demo_gcs_app = SparkSubmitOperator(
        task_id="submit_demo_gcs_app",
        application="/opt/airflow/dags/demo_gcs.py",
        conn_id="my_spark",
    )
