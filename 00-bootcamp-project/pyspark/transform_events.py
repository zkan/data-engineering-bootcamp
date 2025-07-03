import os
from pyspark.sql import SparkSession
from pyspark.sql.types import StructField, StructType, StringType, TimestampType


BUSINESS_DOMAIN = "greenery"
BUCKET_NAME = "deb-bootcamp-999"
DATA = "events"
KEYFILE_PATH = "/opt/spark/pyspark/dataengineercafe-deb-uploading-files-to-gcs-77ed8fc646bf.json"

# execution_date = os.getenv('EXECUTION_DATE')
execution_date = "2021-02-10"

spark = SparkSession.builder.appName("greenery") \
    .config("spark.memory.offHeap.enabled", "true") \
    .config("spark.memory.offHeap.size", "5g") \
    .config("fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem") \
    .config("google.cloud.auth.service.account.enable", "true") \
    .config("google.cloud.auth.service.account.json.keyfile", KEYFILE_PATH) \
    .getOrCreate()

struct_schema = StructType([
    StructField("event_id", StringType()),
    StructField("session_id", StringType()),
    StructField("page_url", StringType()),
    StructField("created_at", TimestampType()),
    StructField("event_type", StringType()),
    StructField("user", StringType()),
    StructField("order", StringType()),
    StructField("product", StringType()),
])

GCS_FILE_PATH = f"gs://{BUCKET_NAME}/raw/{BUSINESS_DOMAIN}/{DATA}/{execution_date}/{DATA}.csv"
df = spark.read.option("header", True).schema(struct_schema).csv(GCS_FILE_PATH)
df.show()

df.createOrReplaceTempView("EVENTS_TABLE")
result = spark.sql("""
    select
        *
    from EVENTS_TABLE
""")


OUTPUT_PATH = f"gs://{BUCKET_NAME}/cleaned/{BUSINESS_DOMAIN}/{DATA}/{execution_date}/"

result.write.mode("overwrite").parquet(OUTPUT_PATH)