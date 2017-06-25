from unittest.mock import MagicMock

from django.test import TestCase

from .services import GmapServices


def get_geocoding_object_with_lat_and_lng(lat, lng):
    return {
        "geometry": {
            "location": {
                "lat": lat,
                "lng": lng
            }
        }
    }


class GmapServicesTest(TestCase):
    def setUp(self):
        self.service = GmapServices()

    def test_geocoding_from_address_return_if_find_one_or_more(self):
        return_value = [get_geocoding_object_with_lat_and_lng(1, 2)]
        client = MagicMock()
        client.get_geocoding.return_value = return_value
        self.service.client = client

        result = self.service.get_geocoding_from_address("address")
        self.assertEqual(len(result), 1)

    def test_geocoding_from_address_none_if_empty(self):
        return_value = []
        client = MagicMock()
        client.get_geocoding.return_value = return_value
        self.service.client = client

        result = self.service.get_geocoding_from_address("address")
        self.assertEqual(result, None)

    def test_geocoding_from_address_when_client_fails(self):
        client = MagicMock()
        client.get_geocoding.return_value = None
        self.service.client = client

        result = self.service.get_geocoding_from_address("address")
        self.assertEqual(result, None)

    def test_get_lat_and_lng_from_address_if_find_one_or_more(self):
        return_value = [get_geocoding_object_with_lat_and_lng(1, 2)]
        client = MagicMock()
        client.get_geocoding.return_value = return_value
        self.service.client = client

        result = self.service.get_lat_and_lng_from_address("address")
        self.assertEqual(result, (1, 2))

    def test_get_lat_and_lng_from_address_get_first_always(self):
        return_value = [get_geocoding_object_with_lat_and_lng(1, 2), get_geocoding_object_with_lat_and_lng(3, 4)]
        client = MagicMock()
        client.get_geocoding.return_value = return_value
        self.service.client = client

        result = self.service.get_lat_and_lng_from_address("address")
        self.assertEqual(result, (1, 2))

    def test_get_lat_and_lng_from_address_none_if_empty(self):
        return_value = []
        client = MagicMock()
        client.get_geocoding.return_value = return_value
        self.service.client = client

        result = self.service.get_geocoding_from_address("address")
        self.assertEqual(result, None)

    def test_get_lat_and_lng_from_address_when_client_fails(self):
        client = MagicMock()
        client.get_geocoding.return_value = None
        self.service.client = client

        result = self.service.get_geocoding_from_address("address")
        self.assertEqual(result, None)
