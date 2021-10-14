from django.contrib.auth.models import User
from django.db import models
from wallet.models import Wallet


class Account(models.Model):
    """Base model"""

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    wallet = models.OneToOneField(Wallet, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} by {self.owner}"

    @property
    def have_assets(self):
        return list(self.wallet.all_assets)


class Broker(Account):
    pass


class Client(Account):
    pass
