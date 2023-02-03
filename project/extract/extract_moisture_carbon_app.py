import logging
import uvicorn
import os
from fastapi import FastAPI, Request
from kafka import KafkaProducer

app = FastAPI()

logger = logging.getLogger()
import json
# Kafka settings
KAFKA_BROKER_URL = os.environ.get("KAFKA_BOOTSTRAP_SERVER")
Producer = KafkaProducer(
            bootstrap_servers=KAFKA_BROKER_URL,
            value_serializer=lambda x: json.dumps(x).encode('utf8'),
            api_version=(0, 10, 1)
        )

@app.post("/collect_moisture_mate")
async def collect_moisture_mate(request: Request):
    received_data = await request.json()
    logger.info(f"Received MoistureMate Data: {received_data}")
    try:
        record = Producer.send('moisturemate', value=received_data)
        logger.info(record)
    except:
        logger.info('didnt run')
    


@app.post("/collect_carbon_sense")
async def collect_carbon_sense(request: Request):
    received_data = await request.json()
    logger.info(f"Received CarbonSense Data: {received_data}")
    try:
        record = Producer.send('carbonsense', value=received_data)
        logger.info(record)
    except:
        logger.info('didnt run')

def run_app():
    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=4008)


if __name__ == "__main__":
    run_app()
