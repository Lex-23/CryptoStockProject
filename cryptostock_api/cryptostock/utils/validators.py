from django.core.validators import validate_email
from notification.models import ConsumerType
from rest_framework.serializers import ValidationError


def validate_is_broker(request):
    if request.auth["user_role"] != "broker":
        raise ValidationError(
            ["You are not a broker. You haven`t permissions for this operation."]
        )


def validate_is_client(request):
    if request.auth["user_role"] != "client":
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


def broker_validate(request, sale):
    validate_is_broker(request)
    broker = request.user.account.broker
    validate_broker_owner_sale(broker, sale)


def validate_asset_count(count, asset, broker):
    sale_count = count
    exists_count = broker.wallet.wallet_record.get(asset=asset).count
    if sale_count > exists_count:
        raise ValidationError([f"You haven`t that much {asset.name}."])


def validate_offer_count(offer_count, deal):
    if offer_count > deal.count:
        raise ValidationError(
            [f"Your offer count: {offer_count} is more then available for this sale."]
        )


def validate_cash_balance(account, deal_value):
    if account.cash_balance < deal_value:
        raise ValidationError(["You don`t have enough funds for this operation."])


def validate_broker_cash_balance(cash_balance, total_price):
    if cash_balance < total_price:
        raise ValidationError(["You don`t have enough funds for this operation."])


def get_validated_asset_from_market(asset_name, market):
    asset = market.client.get_asset(name=asset_name)
    if asset is None:
        raise ValidationError(
            [f"asset {asset_name} not allow for market {market.name}."]
        )
    return asset


def validate_consumer_type(consumer_type: str):
    if consumer_type not in ConsumerType.__members__:
        raise ValidationError([f"consumer type {consumer_type} not implemented."])


def validate_consumer_exists(consumer_type: str, account):
    if account.consumers.filter(type=consumer_type):
        raise ValidationError(
            [f"consumer {consumer_type} exists already for this account."]
        )


def validate_recipient_exists(consumer, recipient):
    if recipient in consumer.data["recipient"]:
        raise ValidationError(
            [f"recipient {recipient} has exists already for this consumer."]
        )


def validate_recipient(recipient):
    try:
        validate_email(recipient)
    except Exception:
        raise ValidationError([f"recipient email {recipient} address not valid ."])
