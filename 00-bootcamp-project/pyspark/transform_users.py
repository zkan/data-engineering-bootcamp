import os
from pyspark.sql import SparkSession
from pyspark.sql.types import StructField, StructType, StringType, TimestampType



BUSINESS_DOMAIN = "greenery"
BUCKET_NAME = "deb-bootcamp-YOUR_STUDENT_ID"
DATA = "users"
KEYFILE_PATH = "YOUR_KEY_FILE_PATH"

execution_date = os.getenv('EXECUTION_DATE')

spark = SparkSession.builder.appName("greenery") \
    .config("spark.memory.offHeap.enabled", "true") \
    .config("spark.memory.offHeap.size", "5g") \
    .config("fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem") \
    .config("google.cloud.auth.service.account.enable", "true") \
    .config("google.cloud.auth.service.account.json.keyfile", KEYFILE_PATH) \
    .getOrCreate()

struct_schema = StructType([
    StructField("user_id",StringType()),
    StructField("first_name",StringType()),
    StructField("last_name",StringType()),
    StructField("email",StringType()),
    StructField("phone_number",StringType()),
    StructField("created_at",TimestampType()),
    StructField("updated_at",TimestampType()),
    StructField("address",StringType()),
])

GCS_FILE_PATH = f"gs://{BUCKET_NAME}/raw/{BUSINESS_DOMAIN}/{DATA}/{execution_date}/{DATA}.csv"
df = spark.read.option("header", True).schema(struct_schema).csv(GCS_FILE_PATH)
df.show()

df.createOrReplaceTempView("USERS_TABLE")
result = spark.sql("""
    select
        *
    from USERS_TABLE
""")


OUTPUT_PATH = f"gs://{BUCKET_NAME}/cleaned/{BUSINESS_DOMAIN}/{DATA}/{execution_date}/"

result.write.mode("overwrite").parquet(OUTPUT_PATH)
