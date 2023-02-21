# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set the working directory to /app
WORKDIR /app

# Install Java
RUN apt-get update && apt-get install -y default-jre

RUN pip install pyspark==3.2.0

# Copy the current directory contents into the container at /app
COPY pyspark_job.py /
COPY . /app

# Environment Variable

ENV PYSPARK_PYTHON=python3
ENV PYSPARK_DRIVER_PYTHON=python3

CMD ["spark-submit", "--master", "local[*]", "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.2", "pyspark_job.py"]
