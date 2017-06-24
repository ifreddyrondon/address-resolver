from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory

from address.models import Address
from address.views import AddressViewSet


class ViewSetTest(TestCase):
    def test_create_view_set(self):
        factory = APIRequestFactory()
        view = AddressViewSet.as_view(actions={'post': 'create'})
        data = {"address": "test address"}
        request = factory.post(reverse('api:address-list'), data)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("address"), data.get("address"))

    def test_list_view_set(self):
        factory = APIRequestFactory()
        view = AddressViewSet.as_view(actions={'get': 'list'})
        address = Address(address="test address")
        address.save()
        address_2 = Address(address="test address 2")
        address_2.save()

        request = factory.get(reverse('api:address-list'))
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0].get("id"), str(address.id))
        self.assertEqual(response.data[0].get("address"), address.address)

    def test_detail_view_set(self):
        factory = APIRequestFactory()
        view = AddressViewSet.as_view(actions={'get': 'retrieve'})
        address = Address(address="test address")
        address.save()

        request = factory.get(reverse('api:address-detail', args=[address.pk]))
        response = view(request, pk=address.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("id"), str(address.id))
        self.assertEqual(response.data.get("address"), address.address)
