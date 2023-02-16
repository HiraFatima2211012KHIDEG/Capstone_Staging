from unittest import TestCase
from unittest.mock import MagicMock, Mock, patch

from lux_meter import lux_meter_service_app


class TestLuxMeterService(TestCase):
    def test_get_latest_record(self):
        luxmeter_data = {"measurements": [1, 2, 3]}

        result = lux_meter_service_app.get_latest_record(luxmeter_data)

        assert result == {"measurements": 3}

    @patch("lux_meter.lux_meter_service_app.requests.get")
    def test_get_data(self, mock_request_get):
        lux_meter_service_app.get_data = Mock()
        lux_meter_service_app.get_data.json.return_value = {
            "test_key": "test_value",
            "measurements": ["test_measurements"],
        }
        mock_request_get.return_value = lux_meter_service_app.get_data

    def test_producer_luxmeter(self):
        lux_meter_service_app.producer_luxmeter = Mock()
        producer_send_test_return_value = "producer_send_test_return_value"
        lux_meter_service_app.producer_luxmeter.send.return_value = (
            producer_send_test_return_value
        )

        assert f"Send luxmeter data to producer: {producer_send_test_return_value}"

    @patch("lux_meter.lux_meter_service_app")
    def test_get_latest_record_response(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "test_key": "test_value",
        }

        mock_requests.get.return_value = mock_response

        self.assertEqual(mock_requests.get.return_value, mock_response)

    @patch("lux_meter.lux_meter_service_app")
    def test_invalid_api(self, mock_requests):
        mock_response = MagicMock()
        mock_response.url = "/invalid_url"
        mock_response.status_code = 404

        mock_requests.get.return_value = mock_response

        self.assertEqual(mock_requests.get.return_value, mock_response)
