import json
import logging
import os

import requests
import uvicorn
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from kafka import KafkaProducer

app = FastAPI()
logger = logging.getLogger()


KAFKA_BROKER_URL = os.environ.get("KAFKA_BOOTSTRAP_SERVER")
URL = os.environ.get("ENDPOINT_URL")

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER_URL,
    value_serializer=lambda x: json.dumps(x).encode("utf8"),
    api_version=(0, 10, 1),
)


@app.on_event("startup")
@repeat_every(seconds=60, wait_first=True)
def periodic():
    for room in ["kitchen", "bedroom", "bathroom", "living_room"]:
        url = URL.format(room)
        producer_luxmeter(url)


def producer_luxmeter(url):
    try:
        record = producer.send("luxmeter", value=get_data(url))
        logger.info(f"Send luxmeter data to producer: {record}")
    except Exception as err:
        logger.exception("Failed to send LuxMeter Data to kafka producer, error:", {err})


def get_data(url: str):
    response = requests.get(url).json()
    logger.info(f"Get data of luxmeter: {response}")
    return get_latest_record(response)


def get_latest_record(luxmeter_data):
    res = luxmeter_data["measurements"][-1]
    luxmeter_data["measurements"] = res
    return luxmeter_data


def run_app():
    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=3007)


if __name__ == "__main__":
    run_app()
