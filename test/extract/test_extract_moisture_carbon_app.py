from unittest import TestCase

from fastapi.testclient import TestClient

from extract.extract_moisture_carbon_app import app

client = TestClient(app)


class TestData(TestCase):
    def test_collect_moisturemate_response_data_log(self):
        with self.assertLogs() as captured:
            response = client.post(
                "/collect_moisture_mate",
                json={"test_key": "test_value"},
            )
        assert response.status_code == 200
        # Check that there is only one message.
        self.assertEqual(len(captured.records), 1)
        # Check that the correct message is logged.
        self.assertEqual(
            captured.records[0].getMessage(),
            "Received MoistureMate data: {'test_key': 'test_value'}",
        )

    def test_collect_carbonsense_response_data_log(self):
        with self.assertLogs() as captured:
            response = client.post(
                "/collect_carbon_sense",
                json={"test_key": "test_value"},
            )
        assert response.status_code == 200
        # Check that there is only one message.
        self.assertEqual(len(captured.records), 1)
        # Check that the correct message is logged.
        self.assertEqual(
            captured.records[0].getMessage(),
            "Received Carbonsense data: {'test_key': 'test_value'}",
        )

    def test_collect_invalidendpoint_response_data_log(self):

        response = client.post(
            "/invalid_endpoint",
            json={"test_key": "test_value"},
        )
        assert response.status_code == 404
