from account.tests.factory import SalesDashboardFactory, WalletRecordFactory


def test_update_sales_dashboard(auth_broker, broker_account):
    wallet_record = WalletRecordFactory(wallet=broker_account.wallet, count="1000")
    asset = wallet_record.asset
    sale = SalesDashboardFactory(
        broker=broker_account, asset=asset, count="500", price="345.543"
    )
    asset_count_before_update = broker_account.wallet.wallet_record.get(
        asset=asset
    ).count
    data = {"count": "615.0000", "price": "320.555780"}

    response = auth_broker.patch(f"/api/salesdashboard/{sale.pk}/", data=data)
    asset_count_after_update = broker_account.wallet.wallet_record.get(
        asset=asset
    ).count
    assert response.status_code == 200
    assert asset_count_after_update == asset_count_before_update
    assert response.json() == {
        "id": sale.id,
        "asset": {
            "id": sale.asset.id,
            "name": sale.asset.name,
            "description": sale.asset.description,
        },
        "count": data["count"],
        "price": data["price"],
        "broker": {
            "id": sale.broker.id,
            "name": sale.broker.name,
            "owner": sale.broker.owner.username,
            "wallet": {"id": sale.broker.wallet.id, "name": sale.broker.wallet.name},
        },
    }
