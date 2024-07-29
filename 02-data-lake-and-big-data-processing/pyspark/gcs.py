from pyspark.sql import SparkSession


KEYFILE_PATH = "/opt/spark/pyspark/YOUR_KEYFILE.json"

# GCS Connector Path: /opt/spark/jars/gcs-connector-hadoop3-latest.jar
spark = SparkSession.builder.appName("demo") \
    .config("spark.jars", "https://storage.googleapis.com/hadoop-lib/gcs/gcs-connector-hadoop3-latest.jar") \
    .config("spark.memory.offHeap.enabled", "true") \
    .config("spark.memory.offHeap.size", "5g") \
    .config("fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem") \
    .config("google.cloud.auth.service.account.enable", "true") \
    .config("google.cloud.auth.service.account.json.keyfile", KEYFILE_PATH) \
    .getOrCreate()

GCS_FILE_PATH = "gs://YOUR_BUCKET_PATH_TO_CSV_FILE"
df = spark.read.option("header", True).csv(GCS_FILE_PATH)
df.show()

df.createOrReplaceTempView("YOUR_TABLE_NAME")
result = spark.sql("""
    select
        *

    from YOUR_TABLE_NAME
""")

OUTPUT_PATH = "gs://YOUR_BUCKET_PATH_TO_OUTPUT"
result.write.mode("overwrite").parquet(OUTPUT_PATH)
