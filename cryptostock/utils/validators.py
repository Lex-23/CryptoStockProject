from account.models import Account
from rest_framework.serializers import ValidationError
from wallet.models import Wallet


def validate_wallet(asset, wal_id):
    wallet = Wallet.objects.get(id=wal_id)
    if asset.wallet.get() != wallet:
        raise ValidationError([f"Error. {asset} not in {wallet}"])


def validate_account(asset, acc_id):
    account = Account.objects.get(id=acc_id)
    if asset.wallet.get().account != account:
        raise ValidationError([f"Error. {asset} not in wallet from {account}"])


def validate_price_type(asset):
    try:
        float(asset.price)
    except ValueError as e:
        raise ValidationError(["this price not numeric"]) from e


def validate_price_positive(asset):
    if float(asset.price) <= 0:
        raise ValidationError(["price must be positive"])
