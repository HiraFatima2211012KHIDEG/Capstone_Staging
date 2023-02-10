import json
import logging
import os

import uvicorn
from fastapi import FastAPI, Request
from kafka import KafkaProducer

logger = logging.getLogger()
app = FastAPI()
KAFKA_BROKER_URL = os.environ.get("KAFKA_BOOTSTRAP_SERVER", "kafka:29092")
# producer is set up in `run_app()` function. We do it to avoid setting it up
# when importing this file as a module, eg. in tests.
producer = None


@app.post("/collect_moisture_mate")
async def collect_moisture_mate(request: Request):
    moisture_data = await request.json()
    logger.info(f"Received MoistureMate data: {moisture_data}")

    try:
        moisture_record = producer.send("moisturemate", value=moisture_data)
        logger.info(f"MoistureMate Data Sent in Kafka: {moisture_record}")
    except Exception as err:
        logger.info(f"Failed to send MoistureMate Data in Kafka: {err}.")


@app.post("/collect_carbon_sense")
async def collect_carbon_sense(request: Request):
    carbon_data = await request.json()
    logger.info(f"Received Carbonsense data: {carbon_data}")

    try:
        carbon_record = producer.send("carbonsense", value=carbon_data)
        logger.info(f"CarbonSense Data Sent in Kafka: {carbon_record}")
    except Exception as err:
        logger.info(f"Failed to send CarbonSense Data in Kafka: {err}.")


def run_app():
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER_URL,
        value_serializer=lambda x: json.dumps(x).encode("utf8"),
        api_version=(0, 10, 1),
    )
    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=4008)


if __name__ == "__main__":
    run_app()
