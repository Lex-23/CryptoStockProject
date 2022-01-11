import decimal
from unittest.mock import MagicMock

import pytest
from account.models import Broker
from account.tests.factory import AssetFactory, WalletRecordFactory
from django.db import connection
from django.test.utils import CaptureQueriesContext
from market.models import YahooMarket
from market.tests.factory import MarketFactory


@pytest.mark.parametrize(
    "asset_name,count", [("BTC", 1), ("BTC", 10), ("ETH", 100), ("DOT1", 1000)]
)
def test_buy_asset_from_market(
    auth_broker, broker_account, assets_list, asset_name, count
):
    market_name = "Yahoo"
    broker_account.cash_balance = decimal.Decimal("10000000.00")
    broker_account.save()
    YahooMarket.get_assets = MagicMock(return_value=assets_list)
    market = MarketFactory(name=market_name)
    deal = market.client.buy(name=asset_name, count=count)
    data = {"count": count}

    cash_balance_before_buy_asset = Broker.objects.get(
        name=broker_account.name
    ).cash_balance
    response = auth_broker.post(
        f"/api/market/{market_name}/asset/{asset_name}/buy/", data=data
    )
    cash_balance_after_buy_asset = Broker.objects.get(
        name=broker_account.name
    ).cash_balance

    assert response.status_code == 201
    assert response.json() == {
        "asset": {
            "name": deal["asset"]["name"],
            "description": deal["asset"]["description"],
            "price": deal["asset"]["price"],
        },
        "count": count,
        "total_price": float(deal["total_price"]),
    }
    assert (
        cash_balance_after_buy_asset
        == cash_balance_before_buy_asset - deal["total_price"]
    )


def test_buy_asset_from_market_broker_have_this_asset_already(
    auth_broker, broker_account, assets_list
):
    """ Case, when broker already have target asset in his wallet """
    market_name = "Yahoo"
    asset_name = "ADA"
    count = 10
    asset = AssetFactory(name=asset_name, description="Cardano")
    broker_wallet_record = WalletRecordFactory(
        asset=asset, wallet=broker_account.wallet
    )
    broker_account.cash_balance = decimal.Decimal("10000000.0000")
    broker_account.save()

    YahooMarket.get_assets = MagicMock(return_value=assets_list)
    MarketFactory(name=market_name)
    data = {"count": count}

    response = auth_broker.post(
        f"/api/market/{market_name}/asset/{asset_name}/buy/", data=data
    )
    assert response.status_code == 201
    assert broker_account.wallet.wallet_record.get(
        asset=asset
    ).count == decimal.Decimal(broker_wallet_record.count) + decimal.Decimal(
        data["count"]
    )


def test_buy_asset_from_market_db_calls(auth_broker, broker_account, assets_list):
    market_name = "Yahoo"
    asset_name = "BTC"
    count = 10
    broker_account.cash_balance = decimal.Decimal("10000000.0000")
    broker_account.save()

    YahooMarket.get_assets = MagicMock(return_value=assets_list)
    MarketFactory(name=market_name)
    data = {"count": count}

    with CaptureQueriesContext(connection) as query_context:
        response = auth_broker.post(
            f"/api/market/{market_name}/asset/{asset_name}/buy/", data=data
        )

    assert response.status_code == 201
    assert len(query_context) == 21


def test_buy_asset_from_market_cash_balance_not_enough(auth_broker, assets_list):
    market_name = "Yahoo"
    asset_name = "BTC"
    count = 100  # broker.cash_balance = 1000 (conftest)

    YahooMarket.get_assets = MagicMock(return_value=assets_list)
    MarketFactory(name=market_name)
    data = {"count": count}

    response = auth_broker.post(
        f"/api/market/{market_name}/asset/{asset_name}/buy/", data=data
    )

    assert response.status_code == 400
    assert response.json() == ["You don`t have enough funds for this operation."]


def test_buy_asset_from_market_not_broker(auth_client):
    market_name = "Yahoo"
    MarketFactory(name=market_name)
    data = {"count": 10}

    response = auth_client.post(f"/api/market/{market_name}/asset/BTC/buy/", data=data)

    assert response.status_code == 400
    assert response.json() == [
        "You are not a broker. You haven`t permissions for this operation."
    ]


def test_buy_nonexistent_asset_from_market_name(auth_broker, assets_list):
    market_name = "Yahoo"
    asset_name = "AnyAsset"
    YahooMarket.get_assets = MagicMock(return_value=assets_list)
    MarketFactory(name=market_name)
    data = {"count": 10}

    response = auth_broker.post(
        f"/api/market/{market_name}/asset/{asset_name}/buy/", data=data
    )

    assert response.status_code == 400
    assert response.json() == [
        f"asset {asset_name} not allow for market {market_name}."
    ]


def test_buy_asset_from_market_not_authenticated_user(api_client):
    name = "Yahoo"

    response = api_client.get(f"/api/market/{name}/asset/BTC/buy/")

    assert response.status_code == 401
