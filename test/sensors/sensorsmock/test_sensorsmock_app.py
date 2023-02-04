import requests

ENDPOINT = "http://0.0.0.0:3000/api/"

def test_collect_response_for_luxmeter():
    """Test the response of the endpoint /luxmeter/{room_id} for the HTTP GET request.

    This function sends an HTTP GET request to the endpoint /luxmeter/{room_id} and checks if the response status code is 200.
    """
    response = requests.get(ENDPOINT + "luxmeter/{room_id}")
    assert response.status_code == 200

def test_collect_response():
    """Test the response of the endpoint /collect for the HTTP POST request.

    This function sends an HTTP POST request to the endpoint /collect with a JSON payload and checks if the response status code is 200.
    """
    response = requests.post(ENDPOINT + "collect",
        json={"test_key": "test_value"},
    )
    assert response.status_code == 200

def test_server_not_found():
    """Test the response for an invalid endpoint for the HTTP POST request.

    This function sends an HTTP POST request to an invalid endpoint and checks if the response status code is 404.
    """
    response = requests.post(ENDPOINT + "invalid_endpoint",
        json={"test_key": "test_value"},
    )
    assert response.status_code == 404