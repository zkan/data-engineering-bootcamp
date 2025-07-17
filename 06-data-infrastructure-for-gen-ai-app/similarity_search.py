import json

from google import genai
from google.cloud import bigquery
from google.oauth2 import service_account


GCP_PROJECT_ID = "YOUR_GCP_PROJECT_ID"
DATASET_ID = "YOUR_DATASET_ID"
TABLE_ID = "YOUR_TABLE_ID"
KEYFILE = "YOUR_KEYFILE"


def get_embedding(client, model: str = "gemini-embedding-exp-03-07", text: str = ""):
    result = client.models.embed_content(
        model=model,
        contents=text,
    )
    return result.embeddings[0]


service_account_info = json.load(open(KEYFILE))
credentials = service_account.Credentials.from_service_account_info(service_account_info)
client = bigquery.Client(
    project=GCP_PROJECT_ID,
    credentials=credentials,
)

vec = get_embedding(client, text="QR codes systems for COVID-19.\nSimple tools for bars, restaurants, offices, and other small proximity businesses.").values

query = f"""
    SELECT
        base.text,
        distance
    FROM
    VECTOR_SEARCH(
        TABLE `{DATASET_ID}.{TABLE_ID}`,
        'embedding',
        (select {vec} as embedding),
        top_k => 3,
        distance_type => 'EUCLIDEAN'
    )
"""

# Run the query
query_job = client.query(query)

# Get the results
results = query_job.result()

# Print the results
for row in results:
    print(row.text)
    print(row.distance)
