from asset.models import Asset
from django.db import models


class Wallet(models.Model):
    assets = models.ManyToManyField(Asset, through="WalletAssistant")
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class WalletAssistant(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    date_joined = models.DateField(auto_now=True)
