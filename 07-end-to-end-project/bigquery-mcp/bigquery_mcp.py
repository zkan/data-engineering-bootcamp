import json
import os

from google.cloud import bigquery
from google.oauth2 import service_account
from mcp.server import MCPServer


GCP_PROJECT_ID = "YOUR_GCP_PROJECT_ID"  # Replace with your GCP project ID
DATASET_ID = "networkrail_reporting"
TABLE_ID = f"{GCP_PROJECT_ID}.{DATASET_ID}.fct_movements"
KEYFILE = "YOUR_KEYFILE_PATH"  # Replace with the path to your service account key file

mcp = MCPServer("BigQuery")

# Set up a BigQuery client
service_account_info = json.load(open(KEYFILE))
credentials = service_account.Credentials.from_service_account_info(service_account_info)
bigquery_client = bigquery.Client(
    project=GCP_PROJECT_ID,
    credentials=credentials,
)


@mcp.tool()
def get_networkrail_movements(limit: int = 100) -> list[dict]:
    """Return up to 100 rows from the permitted movements table."""
    limit = max(1, min(limit, 100))

    sql = f"""
        SELECT *
        FROM `{TABLE_ID}`
        LIMIT @limit
    """
    config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("limit", "INT64", limit),
        ]
    )

    rows = bigquery_client.query(sql, job_config=config).result()
    return [dict(row.items()) for row in rows]


if __name__ == "__main__":
    mcp.run()
