import json
import logging
import os
import pickle

import pandas as pd
from kafka import KafkaConsumer, KafkaProducer

logger = logging.getLogger()

KAFKA_BROKER_URL = os.environ.get("KAFKA_BOOTSTRAP_SERVER")
SAVED_MODEL = os.environ.get("SAVED_MODEL")

model = pickle.load(open(SAVED_MODEL, "rb"))


def predicted_data(consumer, producer):
    for message in consumer:
        logger.info(f"Received message: {message.value}")
        data = json.loads(message.value)
        result = convert_to_json(add_predictions(data))
        logger.info(f"predicted data: {result}")
        send_data_to_producer(result, producer)


def add_predictions(json_data):
    df_data = pd.DataFrame([json_data])
    df_data = df_data.assign(Occupancy=" ")
    df_temp = df_data.drop(["timestamp", "room_id", "Occupancy"], axis=1)

    for index, row in df_temp.iterrows():
        row_array = row.to_numpy()
        result = model.predict([row_array])
        df_data.at[index, "Occupancy"] = result[0]
    return df_data


def convert_to_json(df):
    intal_df = df.to_json(orient="records")
    json_predictions = json.loads(intal_df)
    return json_predictions


def send_data_to_producer(data, producer):
    try:
        record = producer.send("predicted_data", value=data)
        logger.info(f"predicted data sent to kafka topic: {record}")
        producer.flush()
    except Exception as err:
        logger.error(f"Did not Received predicted_data into kafka topic, error:", {err})


if __name__ == "__main__":
    # Create a Kafka consumer
    consumer = KafkaConsumer(
        "merge_sensor_data",
        bootstrap_servers=KAFKA_BROKER_URL,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        value_deserializer=lambda x: x.decode("utf-8"),
        group_id=None,
    )

    # Create a kafka Producer
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER_URL,
        value_serializer=lambda x: json.dumps(x).encode("utf8"),
        api_version=(0, 10, 1),
        acks=1,
    )
    predicted_data(consumer, producer)
