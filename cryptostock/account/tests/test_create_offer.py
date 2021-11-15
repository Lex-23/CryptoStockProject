import decimal

from account.models import Offer, SalesDashboard
from account.tests.factory import (
    BrokerFactory,
    SalesDashboardFactory,
    WalletRecordFactory,
)


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
            asset=wallet_record.asset
        ).count,
        "broker_cash_balance": offer.broker.cash_balance,
        "client_asset_count": offer.client.wallet.wallet_record.get(
            asset=wallet_record.asset
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
        "timestamp": response.json()["timestamp"],
    }
