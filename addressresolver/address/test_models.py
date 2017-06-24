from django.db.models import BooleanField, CharField, DateTimeField, UUIDField
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

    def test_visible_attribute_is_true_by_default(self):
        address = Address.objects.create(address="ejido manzando bajo")
        self.assertTrue(address.visible)

    def test_string_representation(self):
        address = Address.objects.create(address="My address")
        self.assertEqual(str(address), address.address)

