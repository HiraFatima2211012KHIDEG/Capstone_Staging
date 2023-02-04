import requests

ENDPOINT = "http://0.0.0.0:4008"

def test_collect_response_for_moisture_mate_sensor():
    """
    Test the endpoint for collecting moisture data from the moisture mate sensor.
    The test sends a post request to the endpoint with a JSON payload and checks if the returned status code is 200.
    """
    response = requests.post(ENDPOINT + "/collect_moisture_mate",
        json={"test_key": "test_value"},
    )
    assert response.status_code == 200

def test_collect_response_for_carbon_sense():
    """
    Test the endpoint for collecting carbon data from the carbon sense sensor.
    The test sends a post request to the endpoint with a JSON payload and checks if the returned status code is 200.
    """
    response = requests.post(ENDPOINT + "/collect_carbon_sense",
        json={"test_key": "test_value"},
    )
    assert response.status_code == 200


def test_server_not_found():
    """
    Test the endpoint for an invalid endpoint.
    The test sends a post request to an invalid endpoint with a JSON payload and checks if the returned status code is 404.
    """
    response = requests.post(ENDPOINT + "/invalid_endpoint",
        json={"test_key": "test_value"},
    )
    assert response.status_code == 404
