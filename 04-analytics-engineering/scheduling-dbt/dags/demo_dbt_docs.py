from airflow import DAG
from airflow.utils import timezone

from cosmos import ProfileConfig
from cosmos.operators import DbtDocsOperator
from cosmos.profiles import PostgresUserPasswordProfileMapping


"""
# Connections

## Postgres

Connection Id: postgres_dbt
Connection Type: Postgres
Host: postgres
Database: airflow
Login: airflow
Password: airflow
Port 5432
"""

DBT_PROJECT_DIR = "/opt/airflow/dbt/example_dbt_project"

with DAG(
    dag_id="demo_dbt_docs",
    schedule_interval=None,
    start_date=timezone.datetime(2024, 8, 10),
    catchup=False,
    tags=["demo"],
):

    profile_config = ProfileConfig(
        profile_name="example_dbt_project",
        target_name="dev",
        profile_mapping=PostgresUserPasswordProfileMapping(
            conn_id="postgres_dbt",
            profile_args={"schema": "dataset_output"},
        ),
    )

    def upload_docs(project_dir):
        import os

        os.system(f"cp -R {project_dir}/target {DBT_PROJECT_DIR}")


    generate_dbt_docs = DbtDocsOperator(
        task_id="generate_dbt_docs",
        project_dir=DBT_PROJECT_DIR,
        profile_config=profile_config,
        # docs-specific arguments
        callback=upload_docs,
    )
