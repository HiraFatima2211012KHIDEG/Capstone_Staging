from unittest import TestCase
from unittest.mock import Mock

from fastapi.testclient import TestClient

from extract import extract_moisture_carbon_app

client = TestClient(extract_moisture_carbon_app.app)


class TestData(TestCase):
    """
    Class for testing the moisture and carbon data collection from sensors using FastAPI client.
    """

    def test_collect_moisturemate_response_data_log(self):
        """
        Test function to check if the response data from the MoistureMate sensor is correctly collected
        and the received data is correctly logged.
        """
        extract_moisture_carbon_app.producer = Mock()
        producer_send_test_return_value = "producer_send_test_return_value"
        extract_moisture_carbon_app.producer.send.return_value = (
            producer_send_test_return_value
        )
        with self.assertLogs() as captured:
            response = client.post(
                "/collect_moisture_mate",
                json={"test_key": "test_value"},
            )
        assert response.status_code == 200
        # Check that there are two messages: one for receiving the data and
        # one for sending it to Kafka.
        self.assertEqual(len(captured.records), 2)
        # Check that the correct messages are logged.
        self.assertEqual(
            captured.records[0].getMessage(),
            "Received MoistureMate data: {'test_key': 'test_value'}",
        )
        self.assertEqual(
            captured.records[1].getMessage(),
            f"MoistureMate Data Sent in Kafka: {producer_send_test_return_value}",
        )

    def test_collect_carbonsense_response_data_log(self):
        """
        Test function to check if the response data from the CarbonSense sensor is correctly collected
        and the received data is correctly logged.
        """
        extract_moisture_carbon_app.producer = Mock()
        producer_send_test_return_value = "producer_send_test_return_value"
        extract_moisture_carbon_app.producer.send.return_value = (
            producer_send_test_return_value
        )
        with self.assertLogs() as captured:
            response = client.post(
                "/collect_carbon_sense",
                json={"test_key": "test_value"},
            )
        assert response.status_code == 200
        # Check that there are two messages: one for receiving the data and
        # one for sending it to Kafka.
        self.assertEqual(len(captured.records), 2)
        # Check that the correct message is logged.
        self.assertEqual(
            captured.records[0].getMessage(),
            "Received Carbonsense data: {'test_key': 'test_value'}",
        )
        self.assertEqual(
            captured.records[1].getMessage(),
            f"CarbonSense Data Sent in Kafka: {producer_send_test_return_value}",
        )

    def test_collect_moisturemate_producer_raises_logs(self):
        extract_moisture_carbon_app.producer = Mock()
        extract_moisture_carbon_app.producer.send.side_effect = Exception(
            "Test exception"
        )
        with self.assertLogs() as captured:
            response = client.post(
                "/collect_moisture_mate",
                json={"test_key": "test_value"},
            )
        assert response.status_code == 200
        self.assertEqual(len(captured.records), 2)
        self.assertEqual(
            captured.records[0].getMessage(),
            "Received MoistureMate data: {'test_key': 'test_value'}",
        )
        self.assertEqual(
            captured.records[1].getMessage(),
            f"Failed to send MoistureMate Data in Kafka: Test exception.",
        )

    def test_collect_carbonsense_producer_raises_logs(self):
        extract_moisture_carbon_app.producer = Mock()
        extract_moisture_carbon_app.producer.send.side_effect = Exception(
            "Test exception"
        )
        with self.assertLogs() as captured:
            response = client.post(
                "/collect_carbon_sense",
                json={"test_key": "test_value"},
            )
        assert response.status_code == 200
        self.assertEqual(len(captured.records), 2)
        self.assertEqual(
            captured.records[0].getMessage(),
            "Received Carbonsense data: {'test_key': 'test_value'}",
        )
        self.assertEqual(
            captured.records[1].getMessage(),
            f"Failed to send CarbonSense Data in Kafka: Test exception.",
        )

    def test_collect_invalidendpoint_response_data_log(self):
        """
        Test function to check if an error 404 (Not Found) status code is returned when an invalid endpoint is used.
        """
        response = client.post(
            "/invalid_endpoint",
            json={"test_key": "test_value"},
        )
        assert response.status_code == 404
