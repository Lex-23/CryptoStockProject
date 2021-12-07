from unittest.mock import MagicMock

from market.models import Market, YahooMarket
from market.tests.factory import assets_list


def test_get_assets_from_market_name(auth_broker):
    name = "Yahoo"
    YahooMarket.get_assets = MagicMock(return_value=assets_list)
    Market.objects.create(name=name)

    response = auth_broker.get(f"/api/market/{name}/asset/")

    assert response.status_code == 200
    assert response.json() == assets_list
