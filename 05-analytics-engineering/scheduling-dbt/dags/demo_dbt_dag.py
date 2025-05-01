from airflow.utils import timezone

from cosmos import DbtDag, ProjectConfig, ProfileConfig
# from cosmos.profiles import GoogleCloudServiceAccountDictProfileMapping
from cosmos.profiles import PostgresUserPasswordProfileMapping

"""
# Connections

## BigQuery

Connection Id: bigquery_dbt
Connection Type: Google Cloud
Project Id: YOUR_GCP_PROJECT_ID
Keyfile JSON: YOUR_SERVICE_ACCOUNT_JSON

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

# profile_config = ProfileConfig(
#     profile_name="example_dbt_project",
#     target_name="dev",
#     profile_mapping=GoogleCloudServiceAccountDictProfileMapping(
#         conn_id="bigquery_dbt",
#         profile_args={"schema": "dataset_output"},
#     ),
# )

profile_config = ProfileConfig(
    profile_name="example_dbt_project",
    target_name="dev",
    profile_mapping=PostgresUserPasswordProfileMapping(
        conn_id="postgres_dbt",
        profile_args={"schema": "dataset_output"},
    ),
)

example_dbt_project = DbtDag(
    dag_id="demo_dbt_dag",
    schedule_interval=None,
    start_date=timezone.datetime(2022, 11, 27),
    catchup=False,
    project_config=ProjectConfig(DBT_PROJECT_DIR),
    profile_config=profile_config,
    tags=["demo"],
)
