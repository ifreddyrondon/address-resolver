from rest_framework import serializers

from .models import Address


class AddressSerializer(serializers.HyperlinkedModelSerializer):
    elevation = serializers.ReadOnlyField()
    latitude = serializers.ReadOnlyField()
    longitude = serializers.ReadOnlyField()
    url = serializers.HyperlinkedIdentityField(view_name='api:address-detail', read_only=True)

    class Meta:
        model = Address
        fields = ('id', 'url', 'address', 'elevation', 'latitude', 'longitude')
