import requests

ENDPOINT = "http://0.0.0.0:3000/api/"


def test_collect_response_for_luxmeter():
    response = requests.get(ENDPOINT + "luxmeter/{room_id}")
    assert response.status_code == 200


def test_collect_response():
    response = requests.post(
        ENDPOINT + "collect",
        json={"test_key": "test_value"},
    )
    assert response.status_code == 200


def test_server_not_found():
    response = requests.post(
        ENDPOINT + "invalid_endpoint",
        json={"test_key": "test_value"},
    )
    assert response.status_code == 404
