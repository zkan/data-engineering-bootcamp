import os
import time

from google.cloud import bigquery
from google.oauth2 import service_account


def load_data_from_gcs_to_bigquery(gsutil_uri, source_format):
    keyfile = os.environ.get("KEYFILE_PATH")
    bq_client = bigquery.Client(
        credentials=service_account.Credentials.from_service_account_file(
            keyfile
        ),
    )

    # table_id  = project_id + dataset_id + table_name
    table_id = "cultivated-list-383715.greenery.events"
    bq_table = bq_client.get_table(table_id)

    job_config = bigquery.LoadJobConfig(
        schema=bq_table.schema,
        source_format=source_format,
        write_disposition="WRITE_TRUNCATE",
    )
    if ".csv" in gsutil_uri:
        job_config.skip_leading_rows = 1

    start = time.time()
    load_job = bq_client.load_table_from_uri(
        gsutil_uri, table_id, job_config=job_config
    )
    load_job.result()
    end = time.time()

    destination_table = bq_client.get_table(table_id)
    print("Loaded {} rows.".format(destination_table.num_rows))
    print("Loaded data in {}".format(end - start))


if __name__ == "__main__":
    print("CSV format")
    load_data_from_gcs_to_bigquery("gs://example-78147/events.csv", bigquery.SourceFormat.CSV)
    print("\n")

    print("PARQUET format")
    load_data_from_gcs_to_bigquery("gs://example-78147/events.parquet", bigquery.SourceFormat.PARQUET)
    print("\n")

    print("AVRO format")
    load_data_from_gcs_to_bigquery("gs://example-78147/events.avro", bigquery.SourceFormat.AVRO)
