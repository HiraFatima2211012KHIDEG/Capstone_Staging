import pytest
import requests
import json
from extract.extract_moisture_carbon_app import app

from fastapi.testclient import TestClient

client = TestClient(app)

def test_collect_response_for_moisture_mate_sensor():
    response = client.post(
        "/collect_moisture_mate", 
        json={"test_key": "test_value"},
    )
    assert response.status_code == 200

def test_collect_response_for_carbon_sense():
    response = client.post(
        "/collect_carbon_sense", 
        json={"test_key": "test_value"},
    )
    assert response.status_code == 200

def test_server_not_found():
    response = client.post(
        "/invalid_endpoint", 
        json={"test_key": "test_value"},
    )
    assert response.status_code == 404

