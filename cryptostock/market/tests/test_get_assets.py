import os

from market.models import Market


def test_get_assets_from_market_name(auth_broker):
    name = "Yahoo"
    url = os.environ["YAHOO_URL"]
    Market.objects.create(name=name, url=url)

    response = auth_broker.get(f"/api/market/{name}/asset/")

    assert response.status_code == 200
