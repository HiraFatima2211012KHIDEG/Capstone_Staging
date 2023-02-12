import os
import boto3
import json
from kafka import KafkaProducer
from datetime import datetime
from time import sleep
import pandas as pd
import logging


logger = logging.getLogger()


# Connect to the Minio S3-compatible bucket
minio = boto3.client('s3',
                    endpoint_url='http://minio:9000',
                    aws_access_key_id=user_name,
                    aws_secret_access_key=user_password)

# Get the data from the Minio bucket
def minio_key():
    date = datetime.now().replace(second=0, microsecond=0).isoformat()
    return f'smart_thermo/{date}.csv'

sleep(30)
def get_data_from_minio():
    sleep(30)
    data = minio.get_object(Bucket='thermobucketdatabattalion', Key=minio_key())
    initial_df = pd.read_csv(data['Body'])
    logger.info(f"smart thermo data: {initial_df}")
    return initial_df
 
KAFKA_BROKER_URL = os.environ.get("KAFKA_BOOTSTRAP_SERVER")
producer = KafkaProducer(
            bootstrap_servers=KAFKA_BROKER_URL,
            value_serializer=lambda x: json.dumps(x).encode('ascii'),
            api_version=(0, 10, 1),
            acks=1
        )
def send_data_to_kafka():
# Send the data to a Kafka topic
    producer.send(topic='thermo', value=get_data_from_minio().to_json())
    producer.flush()
    logger.info(f"smart thermo data: {get_data_from_minio()}")


