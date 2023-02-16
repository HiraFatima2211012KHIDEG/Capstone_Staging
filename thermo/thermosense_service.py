import os
import boto3
import json
from fastapi import FastAPI
from kafka import KafkaProducer
from datetime import datetime
import pandas as pd
import logging
import uvicorn
from fastapi_utils.tasks import repeat_every

app = FastAPI()
logger = logging.getLogger()

KAFKA_BROKER_URL = os.environ.get("KAFKA_BOOTSTRAP_SERVER")
URL = os.environ.get("ENDPOINT_URL")
BUCKET = os.environ.get("SMART_THERMO_BUCKET")
ACCESS_KEY = os.environ.get("MINIO_ACCESS_KEY")
SECRET_KEY = os.environ.get("MINIO_SECRET_KEY")

@app.on_event("startup")
@repeat_every(seconds=60, wait_first=False)
async def send_data_to_kafka():
    # Connect to the Minio S3-compatible bucket
    minio = boto3.client('s3',
                    endpoint_url=URL,
                    aws_access_key_id=ACCESS_KEY,
                    aws_secret_access_key=SECRET_KEY)


    date = datetime.now().replace(second=0, microsecond=0).isoformat()
    data_key = f'smart_thermo/{date}.csv'
    
    data = minio.get_object(Bucket=BUCKET, Key=data_key)

    initial_df = pd.read_csv(data['Body'],index_col=[0])
    
    logger.info(f"Retrieved smart thermo data from MinIO s3 bucket: {initial_df}")
    initial_df_json = initial_df.to_json()
    final_df = json.loads(initial_df_json)

    df = pd.DataFrame(final_df)

    new_data = df.to_dict(orient="records")
    for row_data in new_data:
        try:
            thermo = producer.send(topic='thermo', value=row_data)
            producer.flush()
            logger.info(f"Smart thermo sense data sent to kafka topic: {thermo}")
        except Exception as err:
            logger.info(f"Failed to send thermo sensse Data in Kafka: {err}.")

def run_app():
    
    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=3010)

if __name__ == "__main__":
    producer = KafkaProducer(
            bootstrap_servers=KAFKA_BROKER_URL,
            value_serializer=lambda x: json.dumps(x).encode('ascii'),
            api_version=(0, 10, 1),
            acks=1
        )
    run_app()
