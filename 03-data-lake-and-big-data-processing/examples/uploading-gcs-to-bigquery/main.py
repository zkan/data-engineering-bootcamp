import os
import time

from google.cloud import bigquery
from google.oauth2 import service_account


GCS_BUCKET = "YOUR_GCS_BUCKET"


def load_data_from_gcs_to_bigquery(gsutil_uri, source_format):
    # keyfile = os.environ.get("KEYFILE_PATH")
    keyfile = "YOUR_KEYFILE_PATH"
    bq_client = bigquery.Client(
        credentials=service_account.Credentials.from_service_account_file(
            keyfile
        ),
    )

    # table_id  = project_id + dataset_id + table_name
    table_id = "YOUR_BIGQUERY_TABLE_ID"
    bq_table = bq_client.get_table(table_id)

    # Check the write disposition in BigQuery here:
    # https://cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.job.LoadJobConfig#google_cloud_bigquery_job_LoadJobConfig_write_disposition
    # Check the time partitioning in BigQuery here:
    # https://cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.job.LoadJobConfig#google_cloud_bigquery_job_LoadJobConfig_time_partitioning
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
    # Check the source format in BigQuery here:
    # https://cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.job.LoadJobConfig#google_cloud_bigquery_job_LoadJobConfig_source_format
    print("CSV format")
    load_data_from_gcs_to_bigquery(f"gs://{GCS_BUCKET}/events.csv", bigquery.SourceFormat.CSV)
    print("\n")

    print("PARQUET format")
    load_data_from_gcs_to_bigquery(f"gs://{GCS_BUCKET}/events.parquet", bigquery.SourceFormat.PARQUET)
    print("\n")

    print("AVRO format")
    load_data_from_gcs_to_bigquery(f"gs://{GCS_BUCKET}/events.avro", bigquery.SourceFormat.AVRO)
