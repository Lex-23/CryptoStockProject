from account.tests.factory import OfferFactory

from cryptostock.settings import REST_FRAMEWORK as DRF


def test_get_offer(auth_user):
    offer = OfferFactory()

    response = auth_user.get(f"/api/offers/{offer.id}/")

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


def test_get_offer_not_authenticated_user(api_client):
    offer = OfferFactory()

    response = api_client.get(f"/api/offers/{offer.id}/")

    assert response.status_code == 401