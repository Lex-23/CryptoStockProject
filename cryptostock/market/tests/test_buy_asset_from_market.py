from unittest.mock import MagicMock

from market.models import YahooMarket
from market.tests.factory import MarketFactory


def test_buy_asset_from_market(auth_broker, broker_account, assets_list):
    # TDD
    market_name = "Yahoo"
    asset_name = "BTC"
    broker_account.cash_balance = "1000000.0000"

    YahooMarket.get_assets = MagicMock(return_value=assets_list)
    MarketFactory(name=market_name)
    data = {"count": 10}

    response = auth_broker.post(
        f"/api/market/{market_name}/asset/{asset_name}/buy/", data=data
    )

    assert response.status_code == 201
