from django.db import models

from addressresolver.core.behaviors import Timestampable, Visiable


class Address(Timestampable, Visiable):
    address = models.CharField(max_length=500)

    def __unicode__(self):
        return self.address

    class Meta:
        ordering = ('address',)
