from django.db import models

from core.behaviors import Timestampable, UUIdable, Visiable


class Address(Timestampable, UUIdable, Visiable):
    address = models.CharField(max_length=500)

    def __str__(self):
        return self.address

    class Meta:
        ordering = ('address',)
