from django.test import TestCase

from unittest.mock import MagicMock, Mock

from gmapservices.client import GmapClient


class OkResult:
    status_code = 200

    @staticmethod
    def json():
        return {
            "results": {
                "something": "ok"
            }
        }


class ErrorResult:
    def __init__(self, status):
        self.status_code = status

    @staticmethod
    def json():
        return {}


class GmapClientTest(TestCase):
    def setUp(self):
        self.client = GmapClient()

    def test_get_geocoding_results_when_is_ok(self):
        abstract_client = MagicMock()
        abstract_client.get.return_value = OkResult()
        self.client.client = abstract_client

        result = self.client.get_geocoding("test")
        self.assertEqual(result, {"something": "ok"})

    def test_get_geocoding_none_when_server_error(self):
        abstract_client = MagicMock()
        abstract_client.get.return_value = ErrorResult(500)
        self.client.client = abstract_client

        result = self.client.get_geocoding("test")
        self.assertEqual(result, None)

    def test_get_geocoding_none_when_client_error(self):
        abstract_client = MagicMock()
        abstract_client.get.return_value = ErrorResult(400)
        self.client.client = abstract_client

        result = self.client.get_geocoding("test")
        self.assertEqual(result, None)

    def test_geocoding_get_none_when_error(self):
        abstract_client = MagicMock()
        abstract_client.get.return_value = Mock(side_effect=Exception)
        self.client.client = abstract_client

        result = self.client.get_geocoding("test")
        self.assertEqual(result, None)

    def test_get_elevation_results_when_is_ok(self):
        abstract_client = MagicMock()
        abstract_client.get.return_value = OkResult()
        self.client.client = abstract_client

        result = self.client.get_elevation("test")
        self.assertEqual(result, {"something": "ok"})

    def test_get_elevation_none_when_server_error(self):
        abstract_client = MagicMock()
        abstract_client.get.return_value = ErrorResult(500)
        self.client.client = abstract_client

        result = self.client.get_elevation("test")
        self.assertEqual(result, None)

    def test_get_elevation_none_when_client_error(self):
        abstract_client = MagicMock()
        abstract_client.get.return_value = ErrorResult(400)
        self.client.client = abstract_client

        result = self.client.get_elevation("test")
        self.assertEqual(result, None)

    def test_elevation_get_none_when_error(self):
        abstract_client = MagicMock()
        abstract_client.get.return_value = Mock(side_effect=Exception)
        self.client.client = abstract_client

        result = self.client.get_elevation("test")
        self.assertEqual(result, None)
