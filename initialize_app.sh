#!/bin/sh

echo "Starting the Kafka broker service..."
docker compose up -d zookeeper
docker compose up -d kafka

echo "Waiting for 20 seconds before starting other services..."
sleep 20

echo "Starting other services..."
docker compose up -d --build
