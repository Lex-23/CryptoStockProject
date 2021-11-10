import decimal


def test_valid_create_sales_dashboard(auth_broker, asset_btc, broker_account):
    asset = asset_btc
    asset_count_before_create = broker_account.wallet.wallet_record.get(
        asset=asset
    ).count
    data = {"asset": asset.id, "count": 100.4444, "price": 500.555555}
    response = auth_broker.post("/api/salesdashboard/", data=data)
    asset_count_after_create = broker_account.wallet.wallet_record.get(
        asset=asset
    ).count
    assert response.status_code == 201
    assert asset_count_after_create == asset_count_before_create
    assert response.json() == {
        "id": 1,
        "asset": {"id": asset.id, "name": asset.name, "description": asset.description},
        "count": str(data["count"]),
        "price": str(data["price"]),
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


def test_invalid_create_sales_dashboard_from_client(auth_client, asset_btc):
    asset = asset_btc
    data = {"asset": asset.id, "count": 100.4444, "price": 500.555555}
    response = auth_client.post("/api/salesdashboard/", data=data)
    assert response.status_code == 400
    assert response.json() == [
        "You are not a broker. You haven`t permissions for this operation."
    ]


def test_invalid_create_sales_dashboard_for_unexists_asset(auth_broker, asset_eth):
    """test for case, when target asset is not exists in broker`s wallet"""
    asset = asset_eth
    data = {"asset": asset.id, "count": 100.4444, "price": 500.555555}
    response = auth_broker.post("/api/salesdashboard/", data=data)
    assert response.status_code == 400
    assert response.json() == [f"You haven't {asset.name} in your wallet."]


def test_invalid_create_sales_dashboard_with_count_more_then_exists(
    auth_broker, asset_btc, broker_account
):
    """test for case, when asset count in input data more then asset count broker has"""
    asset = asset_btc
    data = {
        "asset": asset.id,
        "count": broker_account.wallet.wallet_record.get(asset=asset).count
        + decimal.Decimal("0.0001"),
        "price": 500.555555,
    }
    response = auth_broker.post("/api/salesdashboard/", data=data)
    assert response.status_code == 400
    assert response.json() == [f"You haven`t that much {asset.name}."]