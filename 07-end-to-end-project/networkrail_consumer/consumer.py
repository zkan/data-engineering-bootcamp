import configparser
import json
from datetime import datetime
from time import sleep

from google.cloud import storage
from google.oauth2 import service_account
from kafka import KafkaConsumer


parser = configparser.ConfigParser()
parser.read("confluent.conf")

confluent_bootstrap_servers = parser.get("config", "confluent_bootstrap_servers")
confluent_key = parser.get("config", "confluent_key")
confluent_secret = parser.get("config", "confluent_secret")

GCP_PROJECT_ID = "YOUR_GCP_PROJECT_ID"
BUCKET_NAME = "YOUR_BUCKET_NAME"
BUSINESS_DOMAIN = "networkrail"
DESTINATION_FOLDER = f"{BUSINESS_DOMAIN}/raw"
KEYFILE_PATH = "YOUR_KEYFILE_PATH"
TOPIC = "networkrail-train-movements"
CONSUMER_GROUP = "YOUR_CONSUMER_GROUP"

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=confluent_bootstrap_servers,
    sasl_mechanism="PLAIN",
    security_protocol="SASL_SSL",
    sasl_plain_username=confluent_key,
    sasl_plain_password=confluent_secret,
    group_id=CONSUMER_GROUP,
    auto_offset_reset="earliest",
)

def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    # keyfile = os.environ.get("KEYFILE_PATH")
    keyfile = KEYFILE_PATH
    service_account_info = json.load(open(keyfile))
    credentials = service_account.Credentials.from_service_account_info(service_account_info)
    project_id = GCP_PROJECT_ID

    storage_client = storage.Client(
        project=project_id,
        credentials=credentials,
    )
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)

try:
    for message in consumer:
        try:
            data = json.loads(message.value.decode("utf-8"))
            print(data)

            train_id = data["train_id"]
            now = int(datetime.now().timestamp())
            file_name = f"{train_id}-{now}.json"
            source_file_name = f"data/{file_name}"
            with open(source_file_name, "w") as f:
                json.dump(data, f)

            upload_to_gcs(
                bucket_name=BUCKET_NAME,
                source_file_name=source_file_name,
                destination_blob_name=f"{DESTINATION_FOLDER}/{file_name}",
            )

            sleep(3)
        except json.decoder.JSONDecodeError:
            pass

except KeyboardInterrupt:
    pass
finally:
    consumer.close()
