from airflow.utils import timezone

from cosmos import DbtDag, ProjectConfig, ProfileConfig
from cosmos.profiles import GoogleCloudServiceAccountDictProfileMapping
from cosmos.profiles import PostgresUserPasswordProfileMapping

"""
# Connections

## BigQuery

Connection Id: bigquery_dbt
Connection Type: Google Cloud
Project Id: YOUR_PROJECT_ID
Keyfile JSON: YOUR_SERVICE_ACCOUNT_JSON

"""

DBT_PROJECT_DIR = "/opt/airflow/dbt/greenery"

profile_config = ProfileConfig(
    profile_name="dbt_greenery",
    target_name="dev",
    profile_mapping=GoogleCloudServiceAccountDictProfileMapping(
        conn_id="bigquery_dbt",
        profile_args={"schema": "dbt", "location": "asia-southeast1"},
    ),
)

example_dbt_project = DbtDag(
    dag_id="dbt_greenery",
    schedule_interval=None,
    start_date=timezone.datetime(2022, 11, 27),
    catchup=False,
    project_config=ProjectConfig(DBT_PROJECT_DIR),
    profile_config=profile_config,
    # max_active_tasks=1,
    tags=["demo"],
)
