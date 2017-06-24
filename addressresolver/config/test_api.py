from django.test import TestCase
from django.urls import reverse


class ApiTest(TestCase):
    def test_create_list_uri(self):
        self.assertEqual(reverse('api:address-list'), "/api/address/")

    def test_detail_uri(self):
        self.assertEqual(reverse('api:address-detail', args=['2']), "/api/address/2/")
