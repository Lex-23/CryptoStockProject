from django.db import models
from user.models import User
from wallet.models import Wallet


class Account(models.Model):
    """Base model"""

    owner = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    name = models.CharField(max_length=50)
    wallet = models.OneToOneField(Wallet, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} by {self.owner}"


class Broker(Account):
    pass


class Client(Account):
    pass
