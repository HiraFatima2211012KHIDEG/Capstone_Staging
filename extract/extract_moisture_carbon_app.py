import logging
import os

import uvicorn
from fastapi import FastAPI, Request
from kafka import KafkaProducer

app = FastAPI()

KAFKA_BROKER_URL = os.environ.get("KAFKA_BOOTSTRAP_SERVER")
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER_URL,
    value_serializer=lambda x: json.dumps(x).encode("utf8"),
    api_version=(0, 10, 1),
)

logger = logging.getLogger()
import json


@app.post("/collect_moisture_mate")
async def collect_moisture_mate(request: Request):
    received_data = await request.json()
    logger.info(f"Received MoistureMate Data: {record}")

    try:
        record = producer.send("moisturemate", value=received_data)
        logger.info(f"MoistureMate Data Sent in Kafka: {record}")

    except:
        logger.info("Failed to send MoistureMate Data in Kafka")


@app.post("/collect_carbon_sense")
async def collect_carbon_sense(request: Request):
    received_data = await request.json()
    logger.info(f"Received CarbonSense Data: {record}")

    try:
        record = producer.send("carbonsense", value=received_data)
        logger.info(f"CarbonSense Data Sent in Kafka: {record}")
    except:
        logger.info("Failed to send CarbonSense Data in Kafka")


def run_app():
    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=4008)


if __name__ == "__main__":
    run_app()
