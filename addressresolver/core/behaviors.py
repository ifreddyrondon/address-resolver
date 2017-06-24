import uuid

from django.db import models


class Timestampable(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True


class UUIdable(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Visiable(models.Model):
    visible = models.BooleanField(default=True)

    class Meta:
        abstract = True
