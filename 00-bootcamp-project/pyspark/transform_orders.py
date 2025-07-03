import os
from pyspark.sql import SparkSession
from pyspark.sql.types import FloatType, StructField, StructType, StringType, TimestampType


BUSINESS_DOMAIN = "greenery"
BUCKET_NAME = "deb-bootcamp-999"
DATA = "orders"
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
    StructField("order_id", StringType()),
    StructField("created_at", TimestampType()),
    StructField("order_cost", FloatType()),
    StructField("shipping_cost", FloatType()),
    StructField("order_total", FloatType()),
    StructField("tracking_id", StringType()),
    StructField("shipping_service", StringType()),
    StructField("estimated_delivery_at", TimestampType()),
    StructField("delivered_at", TimestampType()),
    StructField("status", StringType()),
    StructField("user", StringType()),
    StructField("promo", StringType()),
    StructField("address", StringType()),
])

GCS_FILE_PATH = f"gs://{BUCKET_NAME}/raw/{BUSINESS_DOMAIN}/{DATA}/{execution_date}/{DATA}.csv"
df = spark.read.option("header", True).schema(struct_schema).csv(GCS_FILE_PATH)
df.show()

df.createOrReplaceTempView("ORDERS_TABLE")
result = spark.sql("""
    select
        *
    from ORDERS_TABLE
""")


OUTPUT_PATH = f"gs://{BUCKET_NAME}/cleaned/{BUSINESS_DOMAIN}/{DATA}/{execution_date}/"

result.write.mode("overwrite").parquet(OUTPUT_PATH)