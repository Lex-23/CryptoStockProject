from account.tests.factory import (
    BrokerFactory,
    SalesDashboardFactory,
    WalletRecordFactory,
)


def test_create_offer(auth_client):
    broker = BrokerFactory(cash_balance="1000.0000")
    breakpoint()
    wallet_record = WalletRecordFactory(wallet=broker.wallet, count="150.0000")
    sale = SalesDashboardFactory(
        asset=wallet_record.asset, broker=broker, count="55.5555", price="123.9876"
    )
    breakpoint()
    data = {"count": "10.9876"}

    response = auth_client.post(f"/api/salesdashboard/{sale.id}/buy/", data=data)
    breakpoint()
    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "client": {
            "id": 2,
            "name": "Test account client",
            "owner": "tester2",
            "wallet": {"id": 2, "name": "Test Wallet client"},
        },
        "count": "10.9876",
        "deal": {
            "id": 1,
            "asset": {"id": 1, "name": "BTC", "description": "asset_description"},
            "count": "44.5679",
            "price": "123.987600",
            "broker": {
                "id": 3,
                "name": "Another broker",
                "owner": "Katherine",
                "wallet": {"id": 3, "name": "Wallet name"},
            },
        },
        "total_value": 1362.32615376,
        "timestamp": "2021-11-12T16:00:22.630444Z",
    }
