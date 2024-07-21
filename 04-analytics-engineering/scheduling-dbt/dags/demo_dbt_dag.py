from airflow.utils import timezone

from cosmos import DbtDag, ProjectConfig, ProfileConfig
from cosmos.profiles import GoogleCloudServiceAccountDictProfileMapping

"""
#### Connections
1. **bigquery_dbt**
    [
        conn_type=`Google Cloud`,
        keyfile_json=`YOUR_SERVICE_ACCOUNT_JSON`,
        project_id=`YOUR_PROJECT_ID`
    ]
"""

profile_config = ProfileConfig(
    profile_name="example_dbt_project",
    target_name="dev",
    profile_mapping=GoogleCloudServiceAccountDictProfileMapping(
        conn_id="bigquery_dbt",
        profile_args={"schema": "dataset_output"},
    ),
)

example_dbt_project = DbtDag(
    dag_id="demo_dbt_dag",
    schedule_interval="@daily",
    start_date=timezone.datetime(2022, 11, 27),
    catchup=False,
    project_config=ProjectConfig("/opt/airflow/dbt/example_dbt_project"),
    profile_config=profile_config
)
