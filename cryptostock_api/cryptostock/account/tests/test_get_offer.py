from account.tests.factory import OfferFactory, SalesDashboardFactory
from cryptostock.settings import REST_FRAMEWORK as DRF
from django.db import connection
from django.test.utils import CaptureQueriesContext


def test_client_get_offer(auth_client, client_account):
    offer = OfferFactory(client=client_account)

    response = auth_client.get(f"/api/offer/{offer.id}/")

    assert response.status_code == 200
    assert response.json() == {
        "id": offer.id,
        "client": {
            "id": offer.client.id,
            "name": offer.client.name,
            "owner": offer.client.owner.username,
            "wallet": {"id": offer.client.wallet.id, "name": offer.client.wallet.name},
        },
        "count": f"{offer.count}",
        "deal": {
            "id": offer.deal.id,
            "asset": {
                "id": offer.deal.asset.id,
                "name": offer.deal.asset.name,
                "description": offer.deal.asset.description,
            },
            "count": f"{offer.deal.count}",
            "price": f"{offer.price}",
            "broker": {
                "id": offer.broker.id,
                "name": offer.broker.name,
                "owner": offer.broker.owner.username,
                "wallet": {
                    "id": offer.broker.wallet.id,
                    "name": offer.broker.wallet.name,
                },
            },
        },
        "total_value": f"{offer.total_value}",
        "timestamp": f"{offer.timestamp.strftime(format=DRF['DATETIME_FORMAT'])}",
    }


def test_client_get_offer_db_calls(auth_client, client_account):
    offer = OfferFactory(client=client_account)

    with CaptureQueriesContext(connection) as query_context:
        response = auth_client.get(f"/api/offer/{offer.id}/")

    assert response.status_code == 200
    assert len(query_context) == 5


def test_client_get_not_own_offer(auth_client):
    offer = OfferFactory()

    response = auth_client.get(f"/api/offer/{offer.id}/")

    assert response.status_code == 404
    assert response.json() == {"detail": "Not found."}


def test_broker_get_offer(auth_broker, broker_account):
    sale = SalesDashboardFactory(broker=broker_account)
    offer = OfferFactory(deal=sale)

    response = auth_broker.get(f"/api/offer/{offer.id}/")

    assert response.status_code == 200
    assert response.json() == {
        "id": offer.id,
        "client": {
            "id": offer.client.id,
            "name": offer.client.name,
            "owner": offer.client.owner.username,
            "wallet": {"id": offer.client.wallet.id, "name": offer.client.wallet.name},
        },
        "count": f"{offer.count}",
        "deal": {
            "id": offer.deal.id,
            "asset": {
                "id": offer.deal.asset.id,
                "name": offer.deal.asset.name,
                "description": offer.deal.asset.description,
            },
            "count": f"{offer.deal.count}",
            "price": f"{offer.price}",
            "broker": {
                "id": offer.broker.id,
                "name": offer.broker.name,
                "owner": offer.broker.owner.username,
                "wallet": {
                    "id": offer.broker.wallet.id,
                    "name": offer.broker.wallet.name,
                },
            },
        },
        "total_value": f"{offer.total_value}",
        "timestamp": f"{offer.timestamp.strftime(format=DRF['DATETIME_FORMAT'])}",
    }


def test_broker_get_offer_db_calls(auth_broker, broker_account):
    sale = SalesDashboardFactory(broker=broker_account)
    offer = OfferFactory(deal=sale)

    with CaptureQueriesContext(connection) as query_context:
        response = auth_broker.get(f"/api/offer/{offer.id}/")

    assert response.status_code == 200
    assert len(query_context) == 5


def test_broker_get_not_own_offer(auth_broker):
    offer = OfferFactory()

    response = auth_broker.get(f"/api/offer/{offer.id}/")

    assert response.status_code == 404
    assert response.json() == {"detail": "Not found."}


def test_get_offer_not_authenticated_user(api_client):
    offer = OfferFactory()

    response = api_client.get(f"/api/offer/{offer.id}/")

    assert response.status_code == 401
