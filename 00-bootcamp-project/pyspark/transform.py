from pyspark.sql import SparkSession
from pyspark.sql.types import StructField, StructType, StringType, TimestampType


KEYFILE_PATH = "/opt/spark/pyspark/YOUR_KEYFILE.json"

# GCS Connector Path (on Spark): /opt/spark/jars/gcs-connector-hadoop3-latest.jar
# GCS Connector Path (on Airflow): /home/airflow/.local/lib/python3.9/site-packages/pyspark/jars/gcs-connector-hadoop3-latest.jar
# spark = SparkSession.builder.appName("demo") \
#     .config("spark.jars", "https://storage.googleapis.com/hadoop-lib/gcs/gcs-connector-hadoop3-latest.jar") \
#     .config("spark.memory.offHeap.enabled", "true") \
#     .config("spark.memory.offHeap.size", "5g") \
#     .config("fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem") \
#     .config("google.cloud.auth.service.account.enable", "true") \
#     .config("google.cloud.auth.service.account.json.keyfile", KEYFILE_PATH) \
#     .getOrCreate()

spark = SparkSession.builder.appName("transform") \
    .config("spark.memory.offHeap.enabled", "true") \
    .config("spark.memory.offHeap.size", "5g") \
    .config("fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem") \
    .config("google.cloud.auth.service.account.enable", "true") \
    .config("google.cloud.auth.service.account.json.keyfile", KEYFILE_PATH) \
    .getOrCreate()

# --- Data ที่ไม่มี partition

data = "addresses"
GCS_FILE_PATH = f"gs://deb4-bootcamp-00/raw/greenery/{data}/{data}.csv"

struct_schema = StructType([
    StructField("address_id", StringType()),
    StructField("address", StringType()),
    StructField("zipcode", StringType()),
    StructField("state", StringType()),
    StructField("country", StringType()),
])

df = spark.read \
    .option("header", True) \
    .schema(struct_schema) \
    .csv(GCS_FILE_PATH)

df.show()

df.createOrReplaceTempView(data)
result = spark.sql(f"""
    select
        *

    from {data}
""")

OUTPUT_PATH = f"gs://deb4-bootcamp-00/processed/greenery/{data}"
result.write.mode("overwrite").parquet(OUTPUT_PATH)

# --- Data ที่มี partition

data = "users"
dt = "2020-10-23"
GCS_FILE_PATH = f"gs://deb4-bootcamp-00/raw/greenery/{data}/{dt}/{data}.csv"

struct_schema = StructType([
    StructField("user_id", StringType()),
    StructField("first_name", StringType()),
    StructField("last_name", StringType()),
    StructField("email", StringType()),
    StructField("phone_number", StringType()),
    StructField("created_at", TimestampType()),
    StructField("updated_at", TimestampType()),
    StructField("address_id", StringType()),
])

df = spark.read \
    .option("header", True) \
    .schema(struct_schema) \
    .csv(GCS_FILE_PATH)

df.show()

df.createOrReplaceTempView(data)
result = spark.sql(f"""
    select
        *

    from {data}
""")

OUTPUT_PATH = f"gs://deb4-bootcamp-00/processed/greenery/{data}/{dt}"
result.write.mode("overwrite").parquet(OUTPUT_PATH)
