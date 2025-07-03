import os
from pyspark.sql import SparkSession
from pyspark.sql.types import FloatType, IntegerType, StructField, StructType, StringType


BUSINESS_DOMAIN = "greenery"
BUCKET_NAME = "deb-bootcamp-999"
DATA = "products"
KEYFILE_PATH = "/opt/spark/pyspark/dataengineercafe-deb-uploading-files-to-gcs-77ed8fc646bf.json"

execution_date = os.getenv('EXECUTION_DATE')

spark = SparkSession.builder.appName("greenery") \
    .config("spark.memory.offHeap.enabled", "true") \
    .config("spark.memory.offHeap.size", "5g") \
    .config("fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem") \
    .config("google.cloud.auth.service.account.enable", "true") \
    .config("google.cloud.auth.service.account.json.keyfile", KEYFILE_PATH) \
    .getOrCreate()

struct_schema = StructType([
    StructField("product_id", StringType()),
    StructField("name", StringType()),
    StructField("price", FloatType()),
    StructField("inventory", IntegerType()),
])

GCS_FILE_PATH = f"gs://{BUCKET_NAME}/raw/{BUSINESS_DOMAIN}/{DATA}/{DATA}.csv"
df = spark.read.option("header", True).schema(struct_schema).csv(GCS_FILE_PATH)
df.show()

df.createOrReplaceTempView("PRODUCTS_TABLE")
result = spark.sql("""
    select
        *
    from PRODUCTS_TABLE
""")


OUTPUT_PATH = f"gs://{BUCKET_NAME}/cleaned/{BUSINESS_DOMAIN}/{DATA}/"

result.write.mode("overwrite").parquet(OUTPUT_PATH)