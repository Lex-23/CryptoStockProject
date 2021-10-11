from django.db import models
from utils.modules import CustomDecimalField


class AssetType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.name


class Asset(models.Model):
    type = models.ForeignKey(AssetType, on_delete=models.CASCADE)
    price = CustomDecimalField()
    count = CustomDecimalField()

    def __str__(self):
        return f"asset: {self.type.name} for {self.price}"
