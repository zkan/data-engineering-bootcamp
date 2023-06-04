# Ref: https://cloud.google.com/bigquery/docs/samples/bigquery-load-table-dataframe

import json
import os
from datetime import datetime

import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account

# read environment variable
# use export KEYFILE_PATH=deb-1-by-skooldio-36e023357883.json
keyfile = os.environ.get("KEYFILE_PATH")
# read from json file which make service_account_info is json form
service_account_info = json.load(open(keyfile))
credentials = service_account.Credentials.from_service_account_info(service_account_info)
# check your project_id in GCP
project_id = "deb-1-by-skooldio"
client = bigquery.Client(
    project=project_id,
    credentials=credentials,
)

# send JOB to bigquery
job_config = bigquery.LoadJobConfig(
    skip_leading_rows=0,
    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    source_format=bigquery.SourceFormat.CSV,
    autodetect=True,
#     time_partitioning=bigquery.TimePartitioning(
#         type_=bigquery.TimePartitioningType.DAY,
#         field="created_at",
#     ),
#     clustering_fields=["first_name", "last_name"],
)

file_path = "data/order_items.csv"
# tell dataframe which column should be datetime type
df = pd.read_csv(file_path)
df.info()

table_id = f"{project_id}.deb_bootcamp.order_items"
job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
job.result()

# print for debugging
table = client.get_table(table_id)
print(f"Loaded {table.num_rows} rows and {len(table.schema)} columns to {table_id}")