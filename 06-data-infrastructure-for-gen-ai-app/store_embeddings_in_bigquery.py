import json

import pandas as pd
from google import genai
from google.cloud import bigquery
from google.oauth2 import service_account


GCP_PROJECT_ID = "YOUR_GCP_PROJECT_ID"
DATASET_ID = "YOUR_DATASET_ID"
KEYFILE = "YOUR_KEYFILE"
# api_key = os.environ.get("GEMINI_API_KEY")
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"


def get_embedding(client, model: str = "gemini-embedding-exp-03-07", text: str = ""):
    result = client.models.embed_content(
        model=model,
        contents=text,
    )
    return result.embeddings[0]


# Embeddings' part
df = pd.DataFrame(data={
    "text": [
        "QR codes systems for COVID-19.\nSimple tools for bars, restaurants, offices, and other small proximity businesses.",
        "QR code, beacon, and other mobile transactions\nWe have created web and mobile tools which enable both companies and consumers to benefit from mobile transaction technologies (QR codes, beacon, and more). These benefits include mobile commerce, social media, lead generation, analytics, networking, and more. ...",
        "Turning experience into better medicine.\nIodine is creating a massive community of people sharing their experience with what works - and what doesn't - in medicine.\nWe believe Iodine is transforming the consumer experience around health, by providing personal, clear, actionable, and trustworthy resources ...",
    ]
})
print(df.head())

# Set up a Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

df["embedding"] = df.text.map(lambda x: get_embedding(client, text=x).values)
print(df.head())

# BigQuery's part
service_account_info = json.load(open(KEYFILE))
credentials = service_account.Credentials.from_service_account_info(service_account_info)
client = bigquery.Client(
    project=GCP_PROJECT_ID,
    credentials=credentials,
)

schema = [
    bigquery.SchemaField("text", "STRING"),
    bigquery.SchemaField("embedding", "FLOAT64", mode="REPEATED"),
]
job_config = bigquery.LoadJobConfig(
    schema=schema,
    write_disposition="WRITE_TRUNCATE"
)

table_id = f"{GCP_PROJECT_ID}.{DATASET_ID}.my_embeddings"
load_job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
load_job.result()

print(f"Loaded {load_job.output_rows} rows into {DATASET_ID}.{table_id}")
