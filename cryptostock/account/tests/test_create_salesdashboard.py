import decimal

from account.models import SalesDashboard
from account.tests.factory import AssetFactory, WalletRecordFactory


def test_create_sales_dashboard(auth_broker, broker_account):
    wallet_record = WalletRecordFactory(wallet=broker_account.wallet)
    asset = wallet_record.asset
    asset_count_before_create = broker_account.wallet.wallet_record.get(
        asset=asset
    ).count

    data = {"asset": asset.id, "count": "100.4444", "price": "500.555555"}
    response = auth_broker.post("/api/salesdashboard/", data=data)

    created_sale = SalesDashboard.objects.all().last()
    asset_count_after_create = broker_account.wallet.wallet_record.get(
        asset=asset
    ).count

    assert response.status_code == 201
    assert asset_count_after_create == asset_count_before_create
    assert response.json() == {
        "id": created_sale.id,
        "asset": {"id": asset.id, "name": asset.name, "description": asset.description},
        "count": data["count"],
        "price": data["price"],
        "broker": {
            "id": broker_account.id,
            "name": broker_account.name,
            "owner": broker_account.owner.username,
            "wallet": {
                "id": broker_account.wallet.id,
                "name": broker_account.wallet.name,
            },
        },
    }


def test_create_sales_dashboard_not_broker(auth_client):
    asset = AssetFactory()

    data = {"asset": asset.id, "count": "100.4444", "price": "500.555555"}
    response = auth_client.post("/api/salesdashboard/", data=data)

    assert response.status_code == 400
    assert response.json() == [
        "You are not a broker. You haven`t permissions for this operation."
    ]


def test_create_sales_dashboard_asset_not_exist(auth_broker):
    """test for case, when target asset is not exists in broker`s wallet"""
    asset = AssetFactory(name="ETH")

    data = {"asset": asset.id, "count": "100.4444", "price": "500.555555"}
    response = auth_broker.post("/api/salesdashboard/", data=data)

    assert response.status_code == 400
    assert response.json() == [f"You haven't {asset.name} in your wallet."]


def test_create_sales_dashboard_count_too_much(auth_broker, broker_account):
    """test for case, when asset count in input data more then asset count broker has"""
    asset = AssetFactory()
    WalletRecordFactory(wallet=broker_account.wallet, asset=asset)

    data = {
        "asset": asset.id,
        "count": broker_account.wallet.wallet_record.get(asset=asset).count
        + decimal.Decimal("0.0001"),
        "price": "500.555555",
    }
    response = auth_broker.post("/api/salesdashboard/", data=data)

    assert response.status_code == 400
    assert response.json() == [f"You haven`t that much {asset.name}."]
