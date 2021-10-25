import decimal

from rest_framework.serializers import ValidationError


def validate_is_broker(request):
    if not hasattr(request.user.account, "broker"):
        raise ValidationError(
            ["You are not a broker. You haven`t permissions for this operation."]
        )


def validate_is_client(request):
    if not hasattr(request.user.account, "client"):
        raise ValidationError(
            ["You are not a client. You haven`t permissions for this operation."]
        )


def validate_asset_exists(asset, broker):
    if not broker.wallet.wallet_record.filter(asset=asset).exists():
        raise ValidationError([f"You haven't {asset.name} in your wallet."])


def validate_broker_owner_sale(request, sale):
    if request.user.account.broker != sale.broker:
        raise ValidationError(
            ["You haven`t permissions for this operation. This is not your sale."]
        )


def broker_validate(request, sale):
    validate_is_broker(request)
    validate_broker_owner_sale(request, sale)


def validate_asset_count(request, asset, broker):
    data = request.data
    key = "count"
    sale_count = decimal.Decimal(data["count"])
    exists_count = decimal.Decimal(broker.wallet.wallet_record.get(asset=asset).count)

    if key in data and sale_count > exists_count:
        raise ValidationError([f"You haven`t that much {asset.name}."])


def validate_offer_count(serializer, deal):
    offer_count = serializer.data["count"]
    if decimal.Decimal(offer_count) > decimal.Decimal(deal.count):
        raise ValidationError(
            [f"Your offer count: {offer_count} is more then available for this sale."]
        )


def validate_cash_balance(account, deal_value):
    if decimal.Decimal(account.cash_balance) < decimal.Decimal(deal_value):
        raise ValidationError(["You don`t have enough funds for this operation."])
