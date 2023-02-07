import requests

ENDPOINT = "http://0.0.0.0:4008"

def test_collect_response_for_moisture_mate_sensor():
    response = requests.post(ENDPOINT + "/collect_moisture_mate",
        json={"test_key": "test_value"},
    )
    assert response.status_code == 200


def test_collect_response_for_carbon_sense():
    response = requests.post(ENDPOINT + "/collect_carbon_sense",
        json={"test_key": "test_value"},
    )
    assert response.status_code == 200


def test_server_not_found():
    response = requests.post(ENDPOINT + "/invalid_endpoint",
        json={"test_key": "test_value"},
    )
    assert response.status_code == 404
