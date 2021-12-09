from unittest.mock import MagicMock

import pytest
from django.db import connection
from django.test.utils import CaptureQueriesContext
from market.models import YahooMarket
from market.tests.factory import MarketFactory


@pytest.mark.parametrize(
    "asset_name,asset_data",
    [
        ("BTC", {"name": "BTC", "description": "Bitcoin", "price": "50996.99"}),
        ("ETH", {"name": "ETH", "description": "Ethereum", "price": "4353.60"}),
        ("DOT1", {"name": "DOT1", "description": "Polkadot", "price": "28.54"}),
    ],
)
def test_get_asset_from_market_name(auth_broker, assets_list, asset_name, asset_data):
    market_name = "Yahoo"
    YahooMarket.get_assets = MagicMock(return_value=assets_list)
    MarketFactory(name=market_name)

    response = auth_broker.get(f"/api/market/{market_name}/asset/{asset_name}/")

    assert response.status_code == 200
    assert response.json() == asset_data


def test_get_asset_from_market_name_db_calls(auth_broker, assets_list):
    market_name = "Yahoo"
    asset_name = "BTC"
    YahooMarket.get_assets = MagicMock(return_value=assets_list)
    MarketFactory(name=market_name)

    with CaptureQueriesContext(connection) as query_context:
        response = auth_broker.get(f"/api/market/{market_name}/asset/{asset_name}/")

    assert response.status_code == 200
    assert len(query_context) == 2


def test_get_asset_from_market_name_not_broker(auth_client, assets_list):
    market_name = "Yahoo"
    MarketFactory(name=market_name)

    response = auth_client.get(f"/api/market/{market_name}/asset/BTC/")

    assert response.status_code == 400
    assert response.json() == [
        "You are not a broker. You haven`t permissions for this operation."
    ]


def test_get_asset_from_market_not_authenticated_user(api_client):
    name = "Yahoo"

    response = api_client.get(f"/api/market/{name}/asset/BTC/")

    assert response.status_code == 401


def test_get_nonexistent_asset_from_market_name(auth_broker, assets_list):
    market_name = "Yahoo"
    asset_name = "AnyAsset"
    YahooMarket.get_assets = MagicMock(return_value=assets_list)
    MarketFactory(name=market_name)

    response = auth_broker.get(f"/api/market/{market_name}/asset/{asset_name}/")

    assert response.status_code == 400
    assert response.json() == [
        f"asset {asset_name} not allow for market {market_name}."
    ]
