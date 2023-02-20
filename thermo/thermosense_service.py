import json
import logging
import os
from datetime import datetime, timedelta

import boto3
import pandas as pd
import uvicorn
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from kafka import KafkaProducer

app = FastAPI()
logger = logging.getLogger()

KAFKA_BROKER_URL = os.environ.get("KAFKA_BOOTSTRAP_SERVER")
URL = os.environ.get("ENDPOINT_URL")
BUCKET = os.environ.get("SMART_THERMO_BUCKET")
ACCESS_KEY = os.environ.get("MINIO_ACCESS_KEY")
SECRET_KEY = os.environ.get("MINIO_SECRET_KEY")


@app.on_event("startup")
@repeat_every(seconds=60, wait_first=True)
async def send_data_to_kafka():
    # Connect to the Minio S3-compatible bucket
    minio = boto3.client(
        "s3",
        endpoint_url=URL,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
    )

    # Determine the timestamp of the previous minute
    now = datetime.now()
    prev_minute = now - timedelta(minutes=1)
    prev_minute = prev_minute.replace(second=0, microsecond=0).isoformat()

    # Check if there is a file for the previous minute
    prev_minute_key = f"smart_thermo/{prev_minute}.csv"
    try:
        data = minio.get_object(Bucket=BUCKET, Key=prev_minute_key)
    except:
        logger.error(f"No data found for previous minute ({prev_minute}).")
        return

    initial_df = pd.read_csv(data["Body"], index_col=[0]).to_json()

    logger.info(f"Retrieved smart thermo data from MinIO s3 bucket: {initial_df}")

    df = pd.DataFrame(json.loads(initial_df_json))

    new_data = df.to_dict(orient="records")
    for row_data in new_data:
        try:
            thermo = producer.send(topic="thermo", value=row_data)
            producer.flush()
            logger.info(f"Smart thermo sense data sent to kafka topic: {thermo}")
        except Exception as err:
            logger.error(f"Failed to send thermo sensse Data in Kafka: {err}.")


def run_app():
    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=3010)


if __name__ == "__main__":
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER_URL,
        value_serializer=lambda x: json.dumps(x).encode("ascii"),
        api_version=(0, 10, 1),
        acks=0,
    )
    run_app()
