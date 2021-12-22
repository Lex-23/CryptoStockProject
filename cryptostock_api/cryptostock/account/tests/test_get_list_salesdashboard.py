import pytest
from account.tests.factory import AssetFactory, SalesDashboardFactory
from django.db import connection
from django.test.utils import CaptureQueriesContext


def test_get_list_sales_dashboard(auth_user, broker_account):
    sale1 = SalesDashboardFactory(broker=broker_account)
    sale2 = SalesDashboardFactory(broker=broker_account, asset=AssetFactory(name="ETH"))

    response = auth_user.get("/api/salesdashboard/")

    assert response.status_code == 200
    assert response.json()["results"] == [
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
    assert len(query_context) == 3

    SalesDashboardFactory.create_batch(300, broker=broker_account)

    with CaptureQueriesContext(connection) as query_context:
        response = auth_user.get("/api/salesdashboard/")

    assert response.status_code == 200
    assert len(query_context) == 3


@pytest.mark.parametrize(
    "count,limit,offset", [(50, 1, 0), (100, 10, 0), (1000, 10, 2)]
)
def test_get_list_sales_dashboard_pagination_check_limit(
    auth_user, count, limit, offset
):
    SalesDashboardFactory.create_batch(count)

    response = auth_user.get(f"/api/salesdashboard/?limit={limit}&offset={offset}")

    assert response.status_code == 200
    assert response.json().keys() == {"count", "next", "previous", "results"}
    assert response.json()["count"] == count
    assert len(response.json()["results"]) == limit


@pytest.mark.parametrize("limit,offset1,offset2", [(10, 0, 10), (20, 20, 40)])
def test_get_list_sales_dashboard_pagination_check_offset(
    auth_user, limit, offset1, offset2
):
    SalesDashboardFactory.create_batch(100)

    response = auth_user.get(f"/api/salesdashboard/?limit={limit}&offset={offset1}")

    assert response.status_code == 200
    sale_id = response.json()["results"][0]["id"]

    response = auth_user.get(f"/api/salesdashboard/?limit={limit}&offset={offset2}")

    assert response.status_code == 200
    assert response.json()["results"][0]["id"] == sale_id + (offset2 - offset1)


def test_get_list_sales_dashboard_not_authenticated_user(api_client):
    response = api_client.get("/api/salesdashboard/")
    assert response.status_code == 401
