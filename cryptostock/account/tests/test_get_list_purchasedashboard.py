import decimal

import pytest
from account.tests.factory import PurchaseDashboardFactory
from django.db import connection
from django.test.utils import CaptureQueriesContext
from market.tests.factory import MarketFactory

from cryptostock.settings import REST_FRAMEWORK as DRF


def test_get_list_purchasedashboard(auth_broker, broker_account):
    purchase1 = PurchaseDashboardFactory(
        broker=broker_account, market=MarketFactory(name="Yahoo")
    )
    purchase2 = PurchaseDashboardFactory(
        broker=purchase1.broker,
        market=purchase1.market,
        count=decimal.Decimal("20.0000"),
    )
    response = auth_broker.get("/api/purchasedashboard/")

    assert response.status_code == 200
    assert response.json() == {
        "count": 2,
        "next": None,
        "previous": None,
        "results": [
            {
                "asset": {
                    "description": purchase1.asset.description,
                    "id": purchase1.asset.id,
                    "name": purchase1.asset.name,
                },
                "broker": {
                    "id": purchase1.broker.id,
                    "name": purchase1.broker.name,
                    "owner": purchase1.broker.owner.username,
                    "wallet": {
                        "id": purchase1.broker.wallet.id,
                        "name": purchase1.broker.wallet.name,
                    },
                },
                "count": f"{purchase1.count}",
                "id": purchase1.id,
                "market": {
                    "id": purchase1.market.id,
                    "name": purchase1.market.name,
                    "url": purchase1.market.url,
                },
                "price": f"{purchase1.price}",
                "timestamp": f"{purchase1.timestamp.strftime(format=DRF['DATETIME_FORMAT'])}",
            },
            {
                "asset": {
                    "description": purchase2.asset.description,
                    "id": purchase2.asset.id,
                    "name": purchase2.asset.name,
                },
                "broker": {
                    "id": purchase2.broker.id,
                    "name": purchase2.broker.name,
                    "owner": purchase2.broker.owner.username,
                    "wallet": {
                        "id": purchase2.broker.wallet.id,
                        "name": purchase2.broker.wallet.name,
                    },
                },
                "count": f"{purchase2.count}",
                "id": purchase2.id,
                "market": {
                    "id": purchase2.market.id,
                    "name": purchase2.market.name,
                    "url": purchase2.market.url,
                },
                "price": f"{purchase2.price}",
                "timestamp": f"{purchase2.timestamp.strftime(format=DRF['DATETIME_FORMAT'])}",
            },
        ],
    }


def test_get_list_purchasedashboard_db_calls(auth_broker, broker_account):
    PurchaseDashboardFactory.create_batch(10, broker=broker_account)

    with CaptureQueriesContext(connection) as query_context:
        response = auth_broker.get("/api/purchasedashboard/")

    assert response.status_code == 200
    assert len(query_context) == 5

    PurchaseDashboardFactory.create_batch(20, broker=broker_account)

    with CaptureQueriesContext(connection) as query_context:
        response = auth_broker.get("/api/purchasedashboard/")

    assert response.status_code == 200
    assert len(query_context) == 5


@pytest.mark.parametrize("count,limit,offset", [(10, 1, 0), (25, 10, 0), (50, 10, 2)])
def test_get_purchasedashboard_pagination_check_limit(
    auth_broker, broker_account, count, limit, offset
):
    PurchaseDashboardFactory.create_batch(count, broker=broker_account)

    response = auth_broker.get(f"/api/purchasedashboard/?limit={limit}&offset={offset}")

    assert response.status_code == 200
    assert response.json().keys() == {"count", "next", "previous", "results"}
    assert response.json()["count"] == count
    assert len(response.json()["results"]) == limit


@pytest.mark.parametrize("limit,offset1,offset2", [(10, 0, 10), (20, 20, 40)])
def test_get_purchasedashboard_pagination_check_offset(
    auth_broker, broker_account, limit, offset1, offset2
):
    PurchaseDashboardFactory.create_batch(50, broker=broker_account)

    response = auth_broker.get(
        f"/api/purchasedashboard/?limit={limit}&offset={offset1}"
    )

    assert response.status_code == 200
    offer_id = response.json()["results"][0]["id"]

    response = auth_broker.get(
        f"/api/purchasedashboard/?limit={limit}&offset={offset2}"
    )

    assert response.status_code == 200
    assert response.json()["results"][0]["id"] == offer_id + (offset2 - offset1)


def test_get_list_purchasedashboard_not_broker(auth_client):
    PurchaseDashboardFactory()

    response = auth_client.get("/api/purchasedashboard/")

    assert response.status_code == 400
    assert response.json() == [
        "You are not a broker. You haven`t permissions for this operation."
    ]


def test_get_list_purchasedashboard_not_authenticated_user(api_client):
    response = api_client.get("/api/purchasedashboard/")
    assert response.status_code == 401
