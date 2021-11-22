from account.tests.factory import AssetFactory, SalesDashboardFactory
from django.db import connection
from django.test.utils import CaptureQueriesContext


def test_get_list_sales_dashboard(auth_user, broker_account):
    sale1 = SalesDashboardFactory(broker=broker_account)
    sale2 = SalesDashboardFactory(broker=broker_account, asset=AssetFactory(name="ETH"))

    response = auth_user.get("/api/salesdashboard/")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": sale1.id,
            "asset": {
                "id": sale1.asset.id,
                "name": sale1.asset.name,
                "description": sale1.asset.description,
            },
            "count": f"{sale1.count}",
            "price": f"{sale1.price}",
            "broker": {
                "id": sale1.broker.id,
                "name": sale1.broker.name,
                "owner": sale1.broker.owner.username,
                "wallet": {
                    "id": sale1.broker.wallet.id,
                    "name": sale1.broker.wallet.name,
                },
            },
        },
        {
            "id": sale2.id,
            "asset": {
                "id": sale2.asset.id,
                "name": sale2.asset.name,
                "description": sale2.asset.description,
            },
            "count": f"{sale2.count}",
            "price": f"{sale2.price}",
            "broker": {
                "id": sale2.broker.id,
                "name": sale2.broker.name,
                "owner": sale2.broker.owner.username,
                "wallet": {
                    "id": sale2.broker.wallet.id,
                    "name": sale2.broker.wallet.name,
                },
            },
        },
    ]


def test_get_list_sales_dashboard_db_calls(auth_user, broker_account):
    SalesDashboardFactory.create_batch(100, broker=broker_account)

    with CaptureQueriesContext(connection) as query_context:
        response = auth_user.get("/api/salesdashboard/")

    assert response.status_code == 200
    assert len(query_context) == 2

    SalesDashboardFactory.create_batch(1000, broker=broker_account)

    with CaptureQueriesContext(connection) as query_context:
        response = auth_user.get("/api/salesdashboard/")

    assert response.status_code == 200
    assert len(query_context) == 2


def test_get_list_sales_dashboard_not_authenticated_user(api_client):
    response = api_client.get("/api/salesdashboard/")
    assert response.status_code == 401
