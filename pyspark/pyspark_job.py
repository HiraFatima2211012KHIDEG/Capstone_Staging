from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *


def main(spark):
    def process_multiple_topics(topic_dict, schema_dict):
        dfs = {}
        for topic, name in topic_dict.items():
            df = read_stream_data(topic)
            schema = schema_dict[name]
            df = parse_json_data(df, schema)
            dfs[name] = df
        return dfs

    def read_stream_data(topicName):
        df = (
            spark.readStream.format("kafka")
            .option("kafka.bootstrap.servers", "kafka:29092")
            .option("subscribe", topicName)
            .load()
        )
        return df

    def parse_json_data(df, schema):
        df = df.selectExpr("CAST(value AS STRING)")
        df = df.select(from_json(df.value, schema).alias("data"))
        df = df.select("data.*")
        return df

    schema_carbonsense = StructType(
        [
            StructField("room_id", StringType(), True),
            StructField("co2", FloatType(), True),
            StructField("timestamp", TimestampType(), True),
        ]
    )

    schema_moisturemate = StructType(
        [
            StructField("room_id", StringType(), True),
            StructField("timestamp", TimestampType(), True),
            StructField("humidity", FloatType(), True),
            StructField("humidity_ratio", FloatType(), True),
        ]
    )

    schema_luxmeter = StructType(
        [
            StructField("room_id", StringType(), True),
            StructField("measurements", MapType(StringType(), StringType()), True),
        ]
    )

    schema_thermo = StructType(
        [
            StructField("room_id", StringType(), True),
            StructField("temperature", DoubleType(), True),
            StructField("timestamp", TimestampType(), True),
        ]
    )

    topic_dict = {
        "carbonsense": "df_carbonsense",
        "moisturemate": "df_moisturemate",
        "luxmeter": "df_luxmeter",
        "thermo": "df_thermo",
    }

    schema_dict = {
        "df_carbonsense": schema_carbonsense,
        "df_moisturemate": schema_moisturemate,
        "df_luxmeter": schema_luxmeter,
        "df_thermo": schema_thermo,
    }

    dfs = process_multiple_topics(topic_dict, schema_dict)

    df_moisturemate = dfs["df_moisturemate"]
    df_carbonsense = dfs["df_carbonsense"]
    df_luxmeter = dfs["df_luxmeter"]
    df_thermo = dfs["df_thermo"]

    df_luxmeter = (
        df_luxmeter.withColumn(
            "timestamp", col("measurements.timestamp").cast("timestamp")
        )
        .withColumn("light_level", col("measurements.light_level").cast("float"))
        .drop("measurements")
    )

    def fahrenheit_to_celsius(df):
        df = df.withColumn("temperature", expr("(temperature - 32) * 5/9"))
        return df

    df_thermo = fahrenheit_to_celsius(df_thermo)

    def merge_all_sensor_data(df1, df2, df3, df4):
        merge_all_four_sensor_data = (
            df1.join(df2, ["timestamp", "room_id"], "inner")
            .join(df3, ["timestamp", "room_id"], "inner")
            .join(df4, ["timestamp", "room_id"], "inner")
        )
        return merge_all_four_sensor_data

    all_sensor_data = merge_all_sensor_data(
        df_carbonsense, df_moisturemate, df_luxmeter, df_thermo
    )

    new_order = [
        "temperature",
        "humidity",
        "light_level",
        "co2",
        "humidity_ratio",
        "room_id",
        "timestamp",
    ]
    all_sensor_data = all_sensor_data.select(*new_order)

    def data_packed_for_Kafka(df):
        df_to_kafka = df.withColumn(
            "data_packed_for_kafka", to_json(struct(*df.columns))
        )
        df_to_kafka = df_to_kafka.select(col("data_packed_for_kafka").alias("value"))
        return df_to_kafka

    merge_sensor = data_packed_for_Kafka(all_sensor_data)

    def wrting_data_on_kafka_topic(df, topicName, checkpoint, queryName):
        return (
            df.writeStream.format("kafka")
            .option("kafka.bootstrap.servers", "kafka:29092")
            .option("topic", topicName)
            .queryName(queryName)
            .option("checkpointLocation", checkpoint)
            .start()
            .awaitTermination()
        )

    wrting_data_on_kafka_topic(
        merge_sensor, "merge_sensor_data", "checkpoint", "sensor_query"
    )


if __name__ == "__main__":
    spark = (
        SparkSession.builder.master("local[*]")
        .appName("Sensor Data")
        .config(
            "spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.1"
        )
        .getOrCreate()
    )
    main(spark)
