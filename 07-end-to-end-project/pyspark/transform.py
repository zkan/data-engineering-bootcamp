from pyspark.sql import SparkSession
from pyspark.sql.types import StructField, StructType, StringType, TimestampType


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

struct_schema = StructType([
    StructField("actual_timestamp", TimestampType()),
    StructField("auto_expected", StringType()),
    StructField("correction_ind", StringType()),
    StructField("current_train_id", StringType()),
    StructField("delay_monitoring_point", StringType()),
    StructField("direction_ind", StringType()),
    StructField("division_code", StringType()),
    StructField("event_source", StringType()),
    StructField("event_type", StringType()),
    StructField("gbtt_timestamp", TimestampType()),
    StructField("line_ind", StringType()),
    StructField("loc_stanox", StringType()),
    StructField("next_report_run_time", StringType()),
    StructField("next_report_stanox", StringType()),
    StructField("offroute_ind", StringType()),
    StructField("original_loc_stanox", StringType()),
    StructField("original_loc_timestamp", TimestampType()),
    StructField("planned_event_type", StringType()),
    StructField("planned_timestamp", TimestampType()),
    StructField("platform", StringType()),
    StructField("reporting_stanox", StringType()),
    StructField("route", StringType()),
    StructField("timetable_variation", StringType()),
    StructField("toc_id", StringType()),
    StructField("train_id", StringType()),
    StructField("train_file_address", StringType()),
    StructField("train_service_code", StringType()),
    StructField("train_terminated", StringType()),
    StructField("variation_status", StringType()),
])

GCS_FILE_PATH = f"gs://{BUCKET_NAME}/{SOURCE_FOLDER}/*.json"

# df = spark.read \
#     .option("inferSchema", True) \
#     .json(GCS_FILE_PATH)

df = spark.read \
    .schema(struct_schema) \
    .json(GCS_FILE_PATH)

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
