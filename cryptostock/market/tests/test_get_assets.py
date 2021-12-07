from unittest.mock import MagicMock

from market.models import YahooMarket
from market.tests.factory import MarketFactory, assets_list


def test_get_assets_from_market_name(auth_broker):
    name = "Yahoo"
    YahooMarket.get_assets = MagicMock(return_value=assets_list)
    MarketFactory(name=name)
    response = auth_broker.get(f"/api/market/{name}/asset/")

    assert response.status_code == 200
    assert response.json() == assets_list


def test_get_assets_from_market_name_not_broker(auth_client):
    name = "Yahoo"
    MarketFactory(name=name)

    response = auth_client.get(f"/api/market/{name}/asset/")

    assert response.status_code == 400
    assert response.json() == [
        "You are not a broker. You haven`t permissions for this operation."
    ]


def test_get_assets_from_market_not_authenticated_user(api_client):
    name = "Yahoo"

    response = api_client.get(f"/api/market/{name}/asset/")

    assert response.status_code == 401
