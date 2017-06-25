from unittest.mock import MagicMock

from django.contrib.gis.db.models import BooleanField, CharField, DateTimeField, UUIDField, PointField, FloatField
from django.test import TestCase

from address.models import Address


class AddressModelTest(TestCase):
    def test_model_has_id_UUIDField_attribute(self):
        field = Address._meta.get_field("id")
        self.assertTrue(isinstance(field, UUIDField))

    def test_model_has_address_CharField_attribute(self):
        field = Address._meta.get_field("address")
        self.assertTrue(isinstance(field, CharField))

    def test_model_has_created_DateTimeField_attribute(self):
        field = Address._meta.get_field("created")
        self.assertTrue(isinstance(field, DateTimeField))

    def test_model_has_updated_DateTimeField_attribute(self):
        field = Address._meta.get_field("updated")
        self.assertTrue(isinstance(field, DateTimeField))

    def test_model_has_visible_BooleanField_attribute(self):
        field = Address._meta.get_field("visible")
        self.assertTrue(isinstance(field, BooleanField))

    def test_model_has_elevation_FloatField_attribute(self):
        field = Address._meta.get_field("elevation")
        self.assertTrue(isinstance(field, FloatField))

    def test_model_has_location_PointField_attribute(self):
        field = Address._meta.get_field("location")
        self.assertTrue(isinstance(field, PointField))

    def test_visible_attribute_is_true_by_default(self):
        lat, lng = 1, 2
        geo = MagicMock()
        geo.get_lat_and_lng_from_address.return_value = (lat, lng)
        geo.get_elevation_from_lat_and_lng.return_value = 5

        address = Address.objects.create(address="ejido manzando bajo")
        self.assertTrue(address.visible)

    def test_string_representation(self):
        lat, lng = 1, 2
        geo = MagicMock()
        geo.get_lat_and_lng_from_address.return_value = (lat, lng)
        geo.get_elevation_from_lat_and_lng.return_value = 5

        address = Address.objects.create(address="My address")
        self.assertEqual(str(address), address.address)

    def test_raise_error_if_not_lat(self):
        lat, lng = None, 2
        geo = MagicMock()
        geo.get_lat_and_lng_from_address.return_value = (lat, lng)
        geo.get_elevation_from_lat_and_lng.return_value = 1

        Address.objects.create(address="My address")
        self.assertRaises(ValueError)

    def test_raise_error_if_not_lng(self):
        lat, lng = 1, None
        geo = MagicMock()
        geo.get_lat_and_lng_from_address.return_value = (lat, lng)
        geo.get_elevation_from_lat_and_lng.return_value = 1

        Address.objects.create(address="My address")
        self.assertRaises(ValueError)
