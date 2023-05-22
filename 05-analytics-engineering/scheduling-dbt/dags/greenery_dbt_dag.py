from airflow.utils import timezone

from cosmos.providers.dbt import DbtDag


greenery_dbt_project = DbtDag(
    dag_id="greenery_dbt_dag",
    schedule_interval="@daily",
    start_date=timezone.datetime(2022, 11, 27),
    #put your connection id : example_bigquery is created in Airflow by me
    conn_id="example_bigquery",
    catchup=False,
    dbt_project_name="greenery",
    dbt_args={
        "schema": "dbt_mui"
    },
    dbt_root_path="/opt/airflow/dbt",
    tags = ['DEB','2023']
)
