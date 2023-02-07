import logging
from time import sleep
from fastapi import FastAPI
import uvicorn
import requests
import json
import os
from fastapi_utils.tasks import repeat_every
from kafka import KafkaProducer

app = FastAPI()
logger = logging.getLogger()

KAFKA_BROKER_URL = os.environ.get('KAFKA_BOOTSTRAP_SERVER')
Producer = KafkaProducer(
            bootstrap_servers=KAFKA_BROKER_URL,
            value_serializer=lambda x: json.dumps(x).encode('utf8'),
            api_version=(0, 10, 1)
        )

@app.on_event('startup')
@repeat_every(seconds=60, wait_first=True)
def periodic():
    for i in ['kitchen', 'bedroom', 'bathroom', 'living_room']:

        url = f'http://sensorsmock:3003/api/luxmeter/{i}'
        transform(url)


def transform(url: str):
    response = requests.get(url).json()
    res = dict((k, response[k]) for k in ['measurements']
        if k in response)['measurements'][-1]
    response['measurements'] = res
    
    try:
        record = Producer.send('luxmeter', value=response)
        logger.info(f'Received LuxMeter Data: {record}')
    except:
        logger.info('Did not Received LuxMeter Data')
    

def run_app():
    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=3007)


if __name__ == "__main__":
    run_app()