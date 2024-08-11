from pyspark.sql import SparkSession
from pyspark.sql.types import BooleanType, IntegerType, LongType, StructField, StructType, StringType, TimestampType


BUCKET_NAME = "YOUR_BUCKET_NAME"
BUSINESS_DOMAIN = "networkrail"
SOURCE_FOLDER = f"{BUSINESS_DOMAIN}/raw"
DESTINATION_FOLDER = f"{BUSINESS_DOMAIN}/processed"
KEYFILE_PATH = "/opt/spark/pyspark/YOUR_KEYFILE.json"

spark = SparkSession.builder.appName("demo_gcs") \
    .config("spark.memory.offHeap.enabled", "true") \
    .config("spark.memory.offHeap.size", "5g") \
    .config("fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem") \
    .config("google.cloud.auth.service.account.enable", "true") \
    .config("google.cloud.auth.service.account.json.keyfile", KEYFILE_PATH) \
    .getOrCreate()

# struct_schema = StructType([
#     StructField("actual_timestamp", LongType()),
#     StructField("auto_expected", BooleanType()),
#     StructField("correction_ind", BooleanType()),
#     StructField("delay_monitoring_point", BooleanType()),
#     StructField("direction_ind", StringType()),
#     StructField("division_code", IntegerType()),
#     StructField("event_source", StringType()),
#     StructField("event_type", StringType()),
#     StructField("gbtt_timestamp", LongType()),
#     StructField("line_ind", StringType()),
#     StructField("loc_stanox", IntegerType()),
#     StructField("next_report_run_time", IntegerType()),
#     StructField("next_report_stanox", IntegerType()),
#     StructField("offroute_ind", BooleanType()),
#     StructField("planned_event_type", StringType()),
#     StructField("planned_timestamp", LongType()),
#     StructField("platform", IntegerType()),
#     StructField("reporting_stanox", IntegerType()),
#     StructField("route", IntegerType()),
#     StructField("timetable_variation", IntegerType()),
#     StructField("toc_id", IntegerType()),
#     StructField("train_id", StringType()),
#     StructField("train_service_code", IntegerType()),
#     StructField("train_terminated", BooleanType()),
#     StructField("variation_status", StringType()),
# ])

GCS_FILE_PATH = f"gs://{BUCKET_NAME}/{SOURCE_FOLDER}/*.json"

df = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .json(GCS_FILE_PATH)

# df = spark.read \
#     .option("header", True) \
#     .schema(struct_schema) \
#     .json(GCS_FILE_PATH)

df.show()
df.printSchema()

df.createOrReplaceTempView("networkrail")
result = spark.sql("""
    select
        *

    from networkrail
""")

OUTPUT_PATH = f"gs://{BUCKET_NAME}/{DESTINATION_FOLDER}"
result.write.mode("overwrite").parquet(OUTPUT_PATH)
