from django.db import models
from utils.modules import CountField, PriceField


class AssetType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Asset(models.Model):
    type = models.ForeignKey(AssetType, on_delete=models.CASCADE)
    price = PriceField()
    count = CountField()

    def __str__(self):
        return f"{self.count} {self.type.name} for {self.price}"
