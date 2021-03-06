from asset.models import Asset
from django.db import models
from utils.fields import CountField


class Wallet(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class WalletRecord(models.Model):
    asset = models.ForeignKey(
        Asset, on_delete=models.CASCADE, related_name="wallet_record"
    )
    count = CountField()
    wallet = models.ForeignKey(
        Wallet, on_delete=models.CASCADE, related_name="wallet_record"
    )

    class Meta:
        unique_together = ("asset", "wallet")
