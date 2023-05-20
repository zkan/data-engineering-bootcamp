# Ref: https://cloud.google.com/bigquery/docs/samples/bigquery-load-table-gcs-csv

import json
import os

from google.cloud import bigquery
from google.oauth2 import service_account


# keyfile = os.environ.get("KEYFILE_PATH")
keyfile = 'deb-2023-181e69c62d56.json'
service_account_info = json.load(open(keyfile))
credentials = service_account.Credentials.from_service_account_info(service_account_info)
project_id = "deb-2023"  # deb-2023.deb_workshop
client = bigquery.Client(
    project=project_id,
    credentials=credentials,
)

job_config = bigquery.LoadJobConfig(
    skip_leading_rows=1,
    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    source_format=bigquery.SourceFormat.CSV,
    autodetect=True
)

#load data without partition
listfile = os.listdir('data')
for l in listfile:
    file_path = os.path.join('data', l)
    tbname = l.split('.')[0]
    with open(file_path, "rb") as f:
        table_id = f"{project_id}.deb_workshop.{tbname}"
        job = client.load_table_from_file(f, table_id, job_config=job_config)
        job.result()

    table = client.get_table(table_id)
    print(f"Loaded {table.num_rows} rows and {len(table.schema)} columns to {table_id}")

