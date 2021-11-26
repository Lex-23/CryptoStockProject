import decimal as d

import pytest
from account.models import Offer
from account.tests.factory import (
    AssetFactory,
    ClientFactory,
    OfferFactory,
    SalesDashboardFactory,
)
from django.db import connection
from django.test.utils import CaptureQueriesContext

from cryptostock.settings import REST_FRAMEWORK as DRF


def test_client_get_list_offers(auth_client, client_account):
    sale = SalesDashboardFactory()
    offer1 = OfferFactory(deal=sale, client=client_account)
    offer2 = OfferFactory(deal=sale, count=d.Decimal("30.0456"), client=offer1.client)
    OfferFactory(deal=sale, client=ClientFactory())

    response = auth_client.get("/api/offer/")

    assert response.status_code == 200
    assert Offer.objects.count() == 3
    assert len(response.json()["results"]) == 2
    assert response.json()["results"] == [
        {
            "id": offer1.id,
            "client": {
                "id": offer1.client.id,
                "name": offer1.client.name,
                "owner": offer1.client.owner.username,
                "wallet": {
                    "id": offer1.client.wallet.id,
                    "name": offer1.client.wallet.name,
                },
            },
            "count": f"{offer1.count}",
            "deal": {
                "id": offer1.deal.id,
                "asset": {
                    "id": offer1.deal.asset.id,
                    "name": offer1.deal.asset.name,
                    "description": offer1.deal.asset.description,
                },
                "count": f"{offer1.deal.count}",
                "price": f"{offer1.price}",
                "broker": {
                    "id": offer1.broker.id,
                    "name": offer1.broker.name,
                    "owner": offer1.broker.owner.username,
                    "wallet": {
                        "id": offer1.broker.wallet.id,
                        "name": offer1.broker.wallet.name,
                    },
                },
            },
            "total_value": f"{offer1.total_value}",
            "timestamp": f"{offer1.timestamp.strftime(format=DRF['DATETIME_FORMAT'])}",
        },
        {
            "id": offer2.id,
            "client": {
                "id": offer2.client.id,
                "name": offer2.client.name,
                "owner": offer2.client.owner.username,
                "wallet": {
                    "id": offer2.client.wallet.id,
                    "name": offer2.client.wallet.name,
                },
            },
            "count": f"{offer2.count}",
            "deal": {
                "id": offer2.deal.id,
                "asset": {
                    "id": offer2.deal.asset.id,
                    "name": offer2.deal.asset.name,
                    "description": offer2.deal.asset.description,
                },
                "count": f"{offer2.deal.count}",
                "price": f"{offer2.price}",
                "broker": {
                    "id": offer2.broker.id,
                    "name": offer2.broker.name,
                    "owner": offer2.broker.owner.username,
                    "wallet": {
                        "id": offer2.broker.wallet.id,
                        "name": offer2.broker.wallet.name,
                    },
                },
            },
            "total_value": f"{offer2.total_value}",
            "timestamp": f"{offer2.timestamp.strftime(format=DRF['DATETIME_FORMAT'])}",
        },
    ]


def test_broker_get_list_offers(auth_broker, broker_account):
    sale = SalesDashboardFactory(broker=broker_account, asset=AssetFactory(name="ETH"))
    offer1 = OfferFactory(deal=sale)
    offer2 = OfferFactory(deal=sale, count=d.Decimal("30.0456"))
    OfferFactory()

    response = auth_broker.get("/api/offer/")
    assert response.status_code == 200
    assert Offer.objects.count() == 3
    assert len(response.json()["results"]) == 2
    assert response.json()["results"] == [
        {
            "id": offer1.id,
            "client": {
                "id": offer1.client.id,
                "name": offer1.client.name,
                "owner": offer1.client.owner.username,
                "wallet": {
                    "id": offer1.client.wallet.id,
                    "name": offer1.client.wallet.name,
                },
            },
            "count": f"{offer1.count}",
            "deal": {
                "id": offer1.deal.id,
                "asset": {
                    "id": offer1.deal.asset.id,
                    "name": offer1.deal.asset.name,
                    "description": offer1.deal.asset.description,
                },
                "count": f"{offer1.deal.count}",
                "price": f"{offer1.price}",
                "broker": {
                    "id": offer1.broker.id,
                    "name": offer1.broker.name,
                    "owner": offer1.broker.owner.username,
                    "wallet": {
                        "id": offer1.broker.wallet.id,
                        "name": offer1.broker.wallet.name,
                    },
                },
            },
            "total_value": f"{offer1.total_value}",
            "timestamp": f"{offer1.timestamp.strftime(format=DRF['DATETIME_FORMAT'])}",
        },
        {
            "id": offer2.id,
            "client": {
                "id": offer2.client.id,
                "name": offer2.client.name,
                "owner": offer2.client.owner.username,
                "wallet": {
                    "id": offer2.client.wallet.id,
                    "name": offer2.client.wallet.name,
                },
            },
            "count": f"{offer2.count}",
            "deal": {
                "id": offer2.deal.id,
                "asset": {
                    "id": offer2.deal.asset.id,
                    "name": offer2.deal.asset.name,
                    "description": offer2.deal.asset.description,
                },
                "count": f"{offer2.deal.count}",
                "price": f"{offer2.price}",
                "broker": {
                    "id": offer2.broker.id,
                    "name": offer2.broker.name,
                    "owner": offer2.broker.owner.username,
                    "wallet": {
                        "id": offer2.broker.wallet.id,
                        "name": offer2.broker.wallet.name,
                    },
                },
            },
            "total_value": f"{offer2.total_value}",
            "timestamp": f"{offer2.timestamp.strftime(format=DRF['DATETIME_FORMAT'])}",
        },
    ]


def test_get_list_offers_db_calls_from_client(auth_client, client_account):
    OfferFactory.create_batch(100, client=client_account)

    with CaptureQueriesContext(connection) as query_context:
        response = auth_client.get("/api/offer/")

    assert response.status_code == 200
    assert len(query_context) == 6

    OfferFactory.create_batch(1000, client=client_account)

    with CaptureQueriesContext(connection) as query_context:
        response = auth_client.get("/api/offer/")

    assert response.status_code == 200
    assert len(query_context) == 6


def test_get_list_offers_db_calls_from_broker(auth_broker, broker_account):
    sale = SalesDashboardFactory(broker=broker_account)
    OfferFactory.create_batch(100, deal=sale)

    with CaptureQueriesContext(connection) as query_context:
        response = auth_broker.get("/api/offer/")

    assert response.status_code == 200
    assert len(query_context) == 6

    OfferFactory.create_batch(300, deal=sale)

    with CaptureQueriesContext(connection) as query_context:
        response = auth_broker.get("/api/offer/")

    assert response.status_code == 200
    assert len(query_context) == 6


@pytest.mark.parametrize(
    "count,limit,offset", [(50, 1, 0), (100, 10, 0), (1000, 10, 2)]
)
def test_get_offers_pagination_check_limit(
    auth_client, client_account, count, limit, offset
):
    OfferFactory.create_batch(count, client=client_account)

    response = auth_client.get(f"/api/offer/?limit={limit}&offset={offset}")

    assert response.status_code == 200
    assert response.json().keys() == {"count", "next", "previous", "results"}
    assert response.json()["count"] == count
    assert len(response.json()["results"]) == limit


@pytest.mark.parametrize("limit,offset1,offset2", [(10, 0, 10), (20, 20, 40)])
def test_get_offers_pagination_check_offset(
    auth_client, client_account, limit, offset1, offset2
):
    OfferFactory.create_batch(100, client=client_account)

    response = auth_client.get(f"/api/offer/?limit={limit}&offset={offset1}")

    assert response.status_code == 200
    offer_id = response.json()["results"][0]["id"]

    response = auth_client.get(f"/api/offer/?limit={limit}&offset={offset2}")

    assert response.status_code == 200
    assert response.json()["results"][0]["id"] == offer_id + (offset2 - offset1)


def test_get_list_offers_not_authenticated_user(api_client):
    response = api_client.get("/api/offer/")
    assert response.status_code == 401
