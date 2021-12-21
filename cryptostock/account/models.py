import decimal

from asset.models import Asset
from django.contrib.auth.models import User
from django.db import models
from market.models import Market
from utils.fields import CountField, PriceField
from wallet.models import Wallet


class Account(models.Model):
    """Base model"""

    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name="account")
    name = models.CharField(max_length=50)
    wallet = models.OneToOneField(
        Wallet, on_delete=models.CASCADE, related_name="account"
    )
    cash_balance = CountField(max_digits=30, decimal_places=2)
    telegram_chat_id = models.BigIntegerField(
        blank=True,
        null=True,
        help_text="input here 'chat_id' from telegram_bot https://t.me/cryptostock_2021_bot",
    )

    def __str__(self):
        return f"{self.name} ({self.owner})"

    @property
    def wallet_records(self):
        return self.wallet.wallet_record.all()

    @property
    def role(self):
        if hasattr(self, "client"):
            return "client"
        elif hasattr(self, "broker"):
            return "broker"


class Broker(Account):
    pass


class Client(Account):
    pass


class SalesDashboard(models.Model):
    """
    Model for put up for sale assets from broker
    """

    asset = models.ForeignKey(Asset, on_delete=models.DO_NOTHING)
    broker = models.ForeignKey(Broker, on_delete=models.CASCADE)
    count = CountField()
    price = PriceField()
    success_offer_notification = models.BooleanField(
        default=False,
        help_text="turned on notification after every success offer. On default - off.",
    )
    count_control_notification = CountField(
        default=decimal.Decimal("1"),
        help_text="input here min count, after which you want get notification (on default = 1).",
    )

    def __str__(self):
        return f"{self.asset} - price:{self.price} - broker:{self.broker}"


class PurchaseDashboard(models.Model):
    """
    Model for history deals between broker and market
    """

    asset = models.ForeignKey(Asset, on_delete=models.DO_NOTHING)
    market = models.ForeignKey(Market, on_delete=models.DO_NOTHING)
    broker = models.ForeignKey(Broker, on_delete=models.CASCADE)
    price = PriceField()
    count = CountField(decimal_places=0)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.asset} - price: {self.price} - count: {self.count}"


class Offer(models.Model):
    """
    Model for history deals between client and broker
    """

    deal = models.ForeignKey(
        SalesDashboard, on_delete=models.DO_NOTHING, related_name="offer"
    )
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING)
    count = CountField()
    timestamp = models.DateTimeField(auto_now=True)

    @property
    def price(self):
        return self.deal.price

    @property
    def asset(self):
        return self.deal.asset

    @property
    def broker(self):
        return self.deal.broker

    @property
    def total_value(self):
        decimal.getcontext().prec = 24
        return (self.count * self.price).quantize(
            decimal.Decimal("0.01"), rounding=decimal.ROUND_UP
        )
