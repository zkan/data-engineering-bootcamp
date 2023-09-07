from airflow.utils import timezone

from cosmos.providers.dbt import DbtDag


greenery_dbt_project = DbtDag(
    dag_id="greenery_dbt_dag",
    schedule_interval="@daily",
    start_date=timezone.datetime(2023, 9, 3),
    conn_id="deb_bigquery",
    catchup=False,
    dbt_project_name="greenery",
    dbt_args={
        "schema": "dbt_skooldio"
    },
    dbt_root_path="/opt/airflow/dbt",
    tags=["DEB"],
)
