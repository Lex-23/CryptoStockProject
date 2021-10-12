from asset.models import Asset
from django.db import models


class Wallet(models.Model):
    asset = models.ManyToManyField(Asset)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
