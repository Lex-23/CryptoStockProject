from account.tests.factory import SalesDashboardFactory


def test_get_sales_dashboard(auth_user, broker_account):
    sale = SalesDashboardFactory(broker=broker_account)

    response = auth_user.get(f"/api/salesdashboard/{sale.id}/")

    assert response.status_code == 200
    assert response.json() == {
        "id": sale.id,
        "asset": {
            "id": sale.asset.id,
            "name": sale.asset.name,
            "description": sale.asset.description,
        },
        "count": sale.count,
        "price": sale.price,
        "broker": {
            "id": sale.broker.id,
            "name": sale.broker.name,
            "owner": sale.broker.owner.username,
            "wallet": {"id": sale.broker.wallet.id, "name": sale.broker.wallet.name},
        },
    }


def test_get_salesdashboard_not_authenticated_user(api_client, broker_account):
    sale = SalesDashboardFactory(broker=broker_account)
    response = api_client.get(f"/api/salesdashboard/{sale.id}/")

    assert response.status_code == 401
