import configparser
import json
from datetime import datetime
from time import sleep

import stomp
from kafka import KafkaProducer
from pytz import timezone


TIMEZONE_LONDON: timezone = timezone("Europe/London")

parser = configparser.ConfigParser()
parser.read("networkrail.conf")
confluent_bootstrap_servers = parser.get("confluent_config", "confluent_bootstrap_servers")
confluent_key = parser.get("confluent_config", "confluent_key")
confluent_secret = parser.get("confluent_config", "confluent_secret")

producer = KafkaProducer(
    bootstrap_servers=confluent_bootstrap_servers,
    sasl_mechanism="PLAIN",
    security_protocol="SASL_SSL",
    sasl_plain_username=confluent_key,
    sasl_plain_password=confluent_secret,
)


def convert_to_uk_datetime(current_timestamp):
    if current_timestamp is None:
        return None

    timestamp = int(current_timestamp) / 1000
    utc_timestamp = datetime.utcfromtimestamp(timestamp)
    uk_timestamp = TIMEZONE_LONDON.fromutc(utc_timestamp)

    return uk_timestamp


def produce(topic: str, body: dict[str]):
    data = {
        "event_type": body.get("event_type"),
        "gbtt_timestamp": str(convert_to_uk_datetime(body.get("gbtt_timestamp"))),
        "original_loc_stanox": body.get("original_loc_stanox"),
        "planned_timestamp": str(convert_to_uk_datetime(body.get("planned_timestamp"))),
        "timetable_variation": body.get("timetable_variation"),
        "original_loc_timestamp": str(convert_to_uk_datetime(body.get("original_loc_timestamp"))),
        "current_train_id": body.get("current_train_id"),
        "delay_monitoring_point": body.get("delay_monitoring_point"),
        "next_report_run_time": body.get("next_report_run_time"),
        "reporting_stanox": body.get("reporting_stanox"),
        "actual_timestamp": str(convert_to_uk_datetime(body.get("actual_timestamp"))),
        "correction_ind": body.get("correction_ind"),
        "event_source": body.get("event_source"),
        "train_file_address": body.get("train_file_address"),
        "platform": body.get("platform"),
        "division_code": body.get("division_code"),
        "train_terminated": body.get("train_terminated"),
        "train_id": body.get("train_id"),
        "offroute_ind": body.get("offroute_ind"),
        "variation_status": body.get("variation_status"),
        "train_service_code": body.get("train_service_code"),
        "toc_id": body.get("toc_id"),
        "loc_stanox": body.get("loc_stanox"),
        "auto_expected": body.get("auto_expected"),
        "direction_ind": body.get("direction_ind"),
        "route": body.get("direction_ind"),
        "planned_event_type": body.get("planned_event_type"),
        "next_report_stanox": body.get("next_report_stanox"),
        "line_ind": body.get("line_ind"),
    }

    try:
        producer.send(topic, json.dumps(data).encode("utf-8"))
        producer.flush()
    except Exception as e:
        print(f"Error producing message: {e}")


class Listener(stomp.ConnectionListener):
    _mq: stomp.Connection

    def __init__(self, mq: stomp.Connection):
        self._mq = mq

    def on_message(self, frame):
        headers, message_raw = frame.headers, frame.body
        parsed_body = json.loads(message_raw)
        self._mq.ack(id=headers["message-id"], subscription=headers["subscription"])

        for message in parsed_body:
            header = message["header"]
            msg_type = header["msg_type"]
            msg_queue_timestamp = header["msg_queue_timestamp"]
            timestamp = int(msg_queue_timestamp) / 1000
            utc_datetime = datetime.utcfromtimestamp(timestamp)
            uk_datetime = TIMEZONE_LONDON.fromutc(utc_datetime)

            if header["msg_type"] == "0003":
                body = message["body"]
                print(body)
                produce(topic="networkrail-train-movements", body=body)

            print(f"{uk_datetime} - Got a message type of {msg_type} successfully")


if __name__ == "__main__":
    feed_username = parser.get("config", "feed_username")
    feed_password = parser.get("config", "feed_password")

    connection = stomp.Connection(
        [
            ("datafeeds.networkrail.co.uk", 61618)
        ],
        keepalive=True,
        heartbeats=(10000, 10000),
    )
    connection.set_listener("", Listener(connection))

    connection.connect(**{
        "username": feed_username,
        "passcode": feed_password,
        "wait": True,
        "client-id": feed_username,
    })

    # Train Movements feed: https://wiki.openraildata.com/index.php?title=Train_Movements
    connection.subscribe(**{
        "destination": "/topic/TRAIN_MVT_ALL_TOC",
        "id": 1,
        "ack": "client-individual",
        "activemq.subscriptionName": "TRAIN_MVT_ALL_TOC",
    })

    while connection.is_connected():
        sleep(1)
