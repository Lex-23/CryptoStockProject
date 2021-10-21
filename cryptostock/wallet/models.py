from asset.models import Asset
from django.db import models
from utils.modules import CountField


class Wallet(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    @property
    def all_assets(self):
        return self.assets.all()


class WalletRecord(models.Model):
    asset = models.ForeignKey(
        Asset, on_delete=models.CASCADE, related_name="wallet_record", unique=True
    )
    count = CountField(default=0)
    wallet = models.ForeignKey(
        Wallet, on_delete=models.CASCADE, related_name="wallet_record"
    )
