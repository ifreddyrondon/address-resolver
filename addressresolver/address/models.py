from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from rest_framework.exceptions import ValidationError

from core.behaviors import Timestampable, UUIdable, Visiable

from gmapservices.services import GmapServices


class Address(Timestampable, UUIdable, Visiable):
    geo = GmapServices()

    address = models.CharField(max_length=500)
    location = models.PointField(blank=True, null=True)
    elevation = models.FloatField(blank=True, null=True)

    class Meta:
        ordering = ('address',)

    def __str__(self):
        return self.address

    def save(self, *args, **kwargs):
        if self.address:
            lat, lng = self.geo.get_lat_and_lng_from_address(self.address)
            elevation = self.geo.get_elevation_from_lat_and_lng(lat, lng)
            if not lat or not lng:
                raise ValidationError("Latitude, longitude are required")

            self.location = Point(lat, lng)
            if elevation:
                self.elevation = elevation

        super().save(*args, **kwargs)

    @property
    def latitude(self):
        return self.location.x

    @property
    def longitude(self):
        return self.location.y
