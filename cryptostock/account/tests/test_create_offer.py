import decimal as d

from account.models import Offer, SalesDashboard
from account.tests.factory import (
    BrokerFactory,
    SalesDashboardFactory,
    WalletRecordFactory,
)

from cryptostock.settings import REST_FRAMEWORK as DRF


def test_create_offer(auth_client, client_account):
    broker = BrokerFactory(cash_balance=d.Decimal("1000.00"))
    client = client_account
    wallet_record = WalletRecordFactory(wallet=broker.wallet, count=d.Decimal("150.00"))
    sale = SalesDashboardFactory(
        asset=wallet_record.asset,
        broker=broker,
        count=d.Decimal("55.5555"),
        price=d.Decimal("123.98"),
    )
    data = {"count": "10.9876"}

    response = auth_client.post(f"/api/salesdashboard/{sale.id}/buy/", data=data)

    updated_sale = SalesDashboard.objects.get(id=sale.id)
    offer = Offer.objects.all().last()

    assert response.status_code == 201
    assert offer.broker.wallet.wallet_record.get(
        asset=sale.asset
    ).count == wallet_record.count - d.Decimal(data["count"])
    assert offer.client.wallet.wallet_record.get(asset=sale.asset).count == d.Decimal(
        data["count"]
    )
    assert offer.broker.cash_balance == broker.cash_balance + offer.total_value
    assert offer.client.cash_balance == client.cash_balance - offer.total_value
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
            "price": f"{sale.price}",
            "broker": {
                "id": broker.id,
                "name": broker.name,
                "owner": broker.owner.username,
                "wallet": {"id": broker.wallet.id, "name": broker.wallet.name},
            },
        },
        "total_value": f"{offer.total_value}",
        "timestamp": f"{offer.timestamp.strftime(format=DRF['DATETIME_FORMAT'])}",
    }


def test_create_offer_client_have_this_asset(auth_client, client_account):
    """Case, when client already have target asset in his wallet"""
    broker = BrokerFactory(cash_balance=d.Decimal("1000.00"))
    client = client_account
    broker_wallet_record = WalletRecordFactory(
        wallet=broker.wallet, count=d.Decimal("150.0000")
    )
    sale = SalesDashboardFactory(
        asset=broker_wallet_record.asset,
        broker=broker,
        count=d.Decimal("55.5555"),
        price=d.Decimal("123.98"),
    )
    client_wallet_record = WalletRecordFactory(
        wallet=client.wallet, count=d.Decimal("50.0000"), asset=sale.asset
    )
    data = {"count": "10.0000"}

    response = auth_client.post(f"/api/salesdashboard/{sale.id}/buy/", data=data)
    offer = Offer.objects.all().last()

    assert response.status_code == 201
    assert offer.client.wallet.wallet_record.get(
        asset=sale.asset
    ).count == client_wallet_record.count + d.Decimal(data["count"])


def test_create_offer_not_client(auth_broker):
    sale = SalesDashboardFactory()
    data = {"count": "10000.0000"}

    response = auth_broker.post(f"/api/salesdashboard/{sale.id}/buy/", data=data)

    assert response.status_code == 400
    assert response.json() == [
        "You are not a client. You haven`t permissions for this operation."
    ]


def test_create_offer_count_too_much(auth_client):
    sale = SalesDashboardFactory(count=d.Decimal("5.0000"))
    data = {"count": "5.0001"}

    response = auth_client.post(f"/api/salesdashboard/{sale.id}/buy/", data=data)

    assert response.status_code == 400
    assert response.json() == [
        f'Your offer count: {data["count"]} is more then available for this sale.'
    ]


def test_create_offer_cash_balance_not_enough(auth_client):
    sale = SalesDashboardFactory(
        count=d.Decimal("555.0000"), price=d.Decimal("1000.54")
    )
    data = {"count": "500.0000"}  # client.cash_balance = 10000 (conftest)

    response = auth_client.post(f"/api/salesdashboard/{sale.id}/buy/", data=data)

    assert response.status_code == 400
    assert response.json() == ["You don`t have enough funds for this operation."]
