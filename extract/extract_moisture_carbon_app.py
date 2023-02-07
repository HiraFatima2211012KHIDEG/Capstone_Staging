import logging
import uvicorn
import os
from fastapi import FastAPI, Request
from kafka import KafkaProducer
from time import sleep

app = FastAPI()

KAFKA_BROKER_URL = os.environ.get('KAFKA_BOOTSTRAP_SERVER')
Producer = KafkaProducer(
            bootstrap_servers=KAFKA_BROKER_URL,
            value_serializer=lambda x: json.dumps(x).encode('utf8'),
            api_version=(0, 10, 1)
        )

logger = logging.getLogger()
import json

@app.post('/collect_moisture_mate')
async def collect_moisture_mate(request: Request):
    received_data = await request.json()
    try:
        record = Producer.send('moisturemate', value=received_data)
        logger.info(f'Received MoistureMate Data: {record}')
        
    except:
        logger.info('Did not Received MoistureMate Data')

@app.post('/collect_carbon_sense')
async def collect_carbon_sense(request: Request):
    received_data = await request.json()
    
    try:
        record = Producer.send('carbonsense', value=received_data)
        logger.info(f'Received CarbonSense Data: {record}')
    except:
        logger.info('Did not Received CarbonSense Data')
    

def run_app():
    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=4008)


if __name__ == "__main__":
    run_app()
