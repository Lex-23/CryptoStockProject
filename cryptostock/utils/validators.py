import decimal

from account.models import SalesDashboard
from account.serializers import SalesDashboardSerializer
from rest_framework.serializers import ValidationError


def create_sale_object(serializer, asset, broker):
    new_object = SalesDashboard.objects.create(
        asset=asset,
        broker=broker,
        count=serializer.data["count"],
        price=serializer.data["price"],
    )
    serializer_data = SalesDashboardSerializer(new_object).data
    return serializer_data


def validate_price_type(asset):
    try:
        float(asset.price)
    except ValueError as e:
        raise ValidationError(["this price not numeric"]) from e


def validate_price_positive(request):
    if float(request.data["price"]) <= 0:
        raise ValidationError(["price must be positive"])


def validate_is_broker(request):
    if not hasattr(request.user.account, "broker"):
        raise ValidationError(
            ["You are not a broker. You haven`t permissions for this operation."]
        )


def validate_asset_exists(asset, broker):
    if not broker.wallet.wallet_record.filter(asset=asset).exists():
        raise ValidationError([f"You haven't {asset.name} in your wallet."])


def validate_broker_owner_sale(request, sale):
    if request.user.account.broker != sale.broker:
        raise ValidationError(
            ["You haven`t permissions for this operation. This is not your sale."]
        )


def validate_asset_count(request, asset, broker):
    data = request.data
    key = "count"
    sale_count = decimal.Decimal(data["count"])
    exists_count = decimal.Decimal(broker.wallet.wallet_record.get(asset=asset).count)

    if key in data and sale_count > exists_count:
        raise ValidationError([f"You haven`t that much {asset.name}."])
