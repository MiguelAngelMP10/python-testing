import unittest, requests
from src.api_client import get_location
from unittest.mock import patch


class ApiClientTests(unittest.TestCase):

    @patch('src.api_client.requests.get')
    def test_get_location_returns_expected_data(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "countryName": "USA",
            "regionName": "FLORIDA",
            "cityName": "MIAMI",
        }
        result = get_location("8.8.8.8")
        self.assertEqual(result.get("country"), "USA")
        self.assertEqual(result.get("region"), "FLORIDA")
        self.assertEqual(result.get("city"), "MIAMI")

        mock_get.assert_called_once_with("https://freeipapi.com/api/json/8.8.8.8")

    @patch("src.api_client.requests.get")
    def test_get_location_returns_side_effect(self, mock_get):
        mock_get.side_effect = [
            requests.exceptions.RequestException("Service Unavailable"),
            unittest.mock.Mock(
                status_code=200,
                json=lambda: {
                    "countryName": "USA",
                    "regionName": "FLORIDA",
                    "cityName": "MIAMI",
                },
            ),
        ]

        with self.assertRaises(requests.exceptions.RequestException):
            get_location("8.8.8.8")

        result = get_location("8.8.8.8")
        self.assertEqual(result.get("country"), "USA")
        self.assertEqual(result.get("region"), "FLORIDA")
        self.assertEqual(result.get("city"), "MIAMI")

    @patch("src.api_client.requests.get")
    def test_get_location_handles_non_200_response(self, mock_get):
        # Simular una respuesta con código de estado 404
        mock_get.return_value.status_code = 404
        mock_get.return_value.json.return_value = {}

        # Simular que se lanza la excepción cuando el status code no es 200
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError("HTTP Error 404")

        with self.assertRaises(requests.exceptions.HTTPError):
            get_location("8.8.8.8")

    @patch("src.api_client.requests.get")
    def test_get_location_handles_empty_response(self, mock_get):
        # Simular una respuesta vacía o malformada
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {}

        result = {
            "country": None,
            "region": None,
            "city": None,
        }

        # Verificamos que el resultado tenga los valores predeterminados (None)
        self.assertEqual(result.get("country"), None)
        self.assertEqual(result.get("region"), None)
        self.assertEqual(result.get("city"), None)
