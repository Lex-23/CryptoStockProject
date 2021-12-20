from account.tests.factory import PurchaseDashboardFactory
from django.db import connection
from django.test.utils import CaptureQueriesContext
from market.tests.factory import MarketFactory

from cryptostock.settings import REST_FRAMEWORK as DRF


def test_get_purchasedashboard(auth_broker, broker_account):
    purchase = PurchaseDashboardFactory(
        broker=broker_account, market=MarketFactory(name="Yahoo")
    )

    response = auth_broker.get(f"/api/purchasedashboard/{purchase.id}/")

    assert response.status_code == 200
    assert response.json() == {
        "asset": {
            "description": purchase.asset.description,
            "id": purchase.asset.id,
            "name": purchase.asset.name,
        },
        "broker": {
            "id": purchase.broker.id,
            "name": purchase.broker.name,
            "owner": purchase.broker.owner.username,
            "wallet": {
                "id": purchase.broker.wallet.id,
                "name": purchase.broker.wallet.name,
            },
        },
        "count": f"{purchase.count}",
        "id": purchase.id,
        "market": {
            "id": purchase.market.id,
            "name": purchase.market.name,
            "url": purchase.market.url,
        },
        "price": f"{purchase.price}",
        "timestamp": f"{purchase.timestamp.strftime(format=DRF['DATETIME_FORMAT'])}",
    }


def test_get_purchasedashboard_db_calls(auth_broker, broker_account):
    purchase = PurchaseDashboardFactory(
        broker=broker_account, market=MarketFactory(name="Yahoo")
    )

    with CaptureQueriesContext(connection) as query_context:
        response = auth_broker.get(f"/api/purchasedashboard/{purchase.id}/")

    assert response.status_code == 200
    assert len(query_context) == 4


def test_broker_get_not_own_purchasedashboard(auth_broker):
    purchase = PurchaseDashboardFactory()

    response = auth_broker.get(f"/api/purchasedashboard/{purchase.id}/")

    assert response.status_code == 404
    assert response.json() == {"detail": "Not found."}


def test_get_purchasedashboard_not_broker(auth_client):
    purchase = PurchaseDashboardFactory()

    response = auth_client.get(f"/api/purchasedashboard/{purchase.id}/")

    assert response.status_code == 400
    assert response.json() == [
        "You are not a broker. You haven`t permissions for this operation."
    ]


def test_get_purchasedashboard_not_authenticated_user(api_client):
    purchase = PurchaseDashboardFactory()

    response = api_client.get(f"/api/purchasedashboard/{purchase.id}/")

    assert response.status_code == 401
