import decimal as d

from account.tests.factory import OfferFactory, SalesDashboardFactory

from cryptostock.settings import REST_FRAMEWORK as DRF


def test_get_list_offers(auth_user):
    sale = SalesDashboardFactory()
    offer1 = OfferFactory(deal=sale)
    offer2 = OfferFactory(deal=sale, count=d.Decimal("30.0456"))

    response = auth_user.get("/api/offers/")

    assert response.status_code == 200
    assert response.json() == [
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


def test_get_list_offers_not_authenticated_user(api_client):
    response = api_client.get("/api/offers/")
    assert response.status_code == 401
