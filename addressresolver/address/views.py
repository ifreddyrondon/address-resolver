from rest_framework import (mixins, viewsets)

from .models import Address
from .serializers import AddressSerializer


class AddressViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    """
    API endpoint that allows address to be viewed or edited.
    """

    serializer_class = AddressSerializer

    def get_queryset(self):
        return Address.objects.filter(visible=True)
