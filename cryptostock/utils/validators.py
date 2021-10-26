import decimal

from rest_framework.serializers import ValidationError


def validate_is_broker(account):
    if not hasattr(account, "broker"):
        raise ValidationError(
            ["You are not a broker. You haven`t permissions for this operation."]
        )


def validate_is_client(account):
    if not hasattr(account, "client"):
        raise ValidationError(
            ["You are not a client. You haven`t permissions for this operation."]
        )


def validate_asset_exists(asset, broker):
    if not broker.wallet.wallet_record.filter(asset=asset).exists():
        raise ValidationError([f"You haven't {asset.name} in your wallet."])


def validate_broker_owner_sale(broker, sale):
    if broker != sale.broker:
        raise ValidationError(
            ["You haven`t permissions for this operation. This is not your sale."]
        )


def broker_validate(account, sale):
    validate_is_broker(account)
    broker = account.broker
    validate_broker_owner_sale(broker, sale)


def validate_asset_count(count, asset, broker):
    sale_count = decimal.Decimal(count)
    exists_count = decimal.Decimal(broker.wallet.wallet_record.get(asset=asset).count)
    if sale_count > exists_count:
        raise ValidationError([f"You haven`t that much {asset.name}."])


def validate_offer_count(offer_count, deal):
    if decimal.Decimal(offer_count) > decimal.Decimal(deal.count):
        raise ValidationError(
            [f"Your offer count: {offer_count} is more then available for this sale."]
        )


def validate_cash_balance(account, deal_value):
    if decimal.Decimal(account.cash_balance) < decimal.Decimal(deal_value):
        raise ValidationError(["You don`t have enough funds for this operation."])
