import decimal

from account.models import Offer, SalesDashboard
from account.tests.factory import (
    BrokerFactory,
    SalesDashboardFactory,
    WalletRecordFactory,
)

from cryptostock.settings import REST_FRAMEWORK as DRF


def test_create_offer(auth_client, client_account):
    broker = BrokerFactory(cash_balance="1000.0000")
    client = client_account
    wallet_record = WalletRecordFactory(wallet=broker.wallet, count="150.0000")
    sale = SalesDashboardFactory(
        asset=wallet_record.asset, broker=broker, count="55.5555", price="123.987600"
    )
    data = {"count": "10.9876"}
    check_total_value = (
        f'{(round((decimal.Decimal(sale.price) * decimal.Decimal(data["count"])), 4))}'
    )

    response = auth_client.post(f"/api/salesdashboard/{sale.id}/buy/", data=data)

    updated_sale = SalesDashboard.objects.get(id=sale.id)
    offer = Offer.objects.all().last()
    offer_result = {
        "broker_asset_count": offer.broker.wallet.wallet_record.get(
            asset=sale.asset
        ).count,
        "broker_cash_balance": offer.broker.cash_balance,
        "client_asset_count": offer.client.wallet.wallet_record.get(
            asset=sale.asset
        ).count,
        "client_cash_balance": offer.client.cash_balance,
    }

    assert response.status_code == 201
    assert offer_result["broker_asset_count"] == (
        decimal.Decimal(wallet_record.count) - decimal.Decimal(data["count"])
    )
    assert offer_result["client_asset_count"] == decimal.Decimal(data["count"])
    assert offer_result["broker_cash_balance"] == decimal.Decimal(
        broker.cash_balance
    ) + decimal.Decimal(check_total_value)
    assert offer_result["client_cash_balance"] == decimal.Decimal(
        client.cash_balance
    ) - decimal.Decimal(check_total_value)
    assert response.json() == {
        "id": offer.id,
        "client": {
            "id": client.id,
            "name": client.name,
            "owner": client.owner.username,
            "wallet": {"id": client.wallet.id, "name": client.wallet.name},
        },
        "count": data["count"],
        "deal": {
            "id": sale.id,
            "asset": {
                "id": sale.asset.id,
                "name": sale.asset.name,
                "description": sale.asset.description,
            },
            "count": f"{updated_sale.count}",
            "price": sale.price,
            "broker": {
                "id": broker.id,
                "name": broker.name,
                "owner": broker.owner.username,
                "wallet": {"id": broker.wallet.id, "name": broker.wallet.name},
            },
        },
        "total_value": check_total_value,
        "timestamp": f"{offer.timestamp.strftime(format=DRF['DATETIME_FORMAT'])}",
    }


def test_create_offer_client_have_this_asset(auth_client, client_account):
    """Case, when client already have target asset in his wallet"""
    broker = BrokerFactory(cash_balance="1000.0000")
    client = client_account
    broker_wallet_record = WalletRecordFactory(wallet=broker.wallet, count="150.0000")
    sale = SalesDashboardFactory(
        asset=broker_wallet_record.asset,
        broker=broker,
        count="55.5555",
        price="123.987600",
    )
    client_wallet_record = WalletRecordFactory(
        wallet=client.wallet, count="50.0000", asset=sale.asset
    )
    data = {"count": "10.0000"}

    response = auth_client.post(f"/api/salesdashboard/{sale.id}/buy/", data=data)
    offer = Offer.objects.all().last()

    assert response.status_code == 201
    assert offer.client.wallet.wallet_record.get(
        asset=sale.asset
    ).count == decimal.Decimal(client_wallet_record.count) + decimal.Decimal(
        data["count"]
    )


def test_create_offer_not_client(auth_broker):
    sale = SalesDashboardFactory()
    data = {"count": "10000.0000"}

    response = auth_broker.post(f"/api/salesdashboard/{sale.id}/buy/", data=data)

    assert response.status_code == 400
    assert response.json() == [
        "You are not a client. You haven`t permissions for this operation."
    ]


def test_create_offer_count_too_much(auth_client):
    sale = SalesDashboardFactory(count="5.0000")
    data = {"count": "5.0001"}

    response = auth_client.post(f"/api/salesdashboard/{sale.id}/buy/", data=data)

    assert response.status_code == 400
    assert response.json() == [
        f'Your offer count: {data["count"]} is more then available for this sale.'
    ]


def test_create_offer_cash_balance_not_enough(auth_client):
    sale = SalesDashboardFactory(count="555.0000", price="1000.548796")
    data = {"count": "500.0000"}  # client.cash_balance = 10000 (conftest)

    response = auth_client.post(f"/api/salesdashboard/{sale.id}/buy/", data=data)

    assert response.status_code == 400
    assert response.json() == ["You don`t have enough funds for this operation."]
