import decimal

from account.tests.factory import PurchaseDashboardFactory
from django.db import connection
from django.test.utils import CaptureQueriesContext
from market.tests.factory import MarketFactory


def test_get_list_purchasedashboard(auth_broker, broker_account):
    purchase1 = PurchaseDashboardFactory(
        broker=broker_account, market=MarketFactory(name="Yahoo", url="http//:url")
    )
    PurchaseDashboardFactory(
        broker=purchase1.broker,
        market=purchase1.market,
        count=decimal.Decimal("20.0000"),
    )

    response = auth_broker.get("/api/purchasedashboard/")

    assert response.status_code == 200


def test_get_list_purchasedashboard_db_calls(auth_broker, broker_account):
    PurchaseDashboardFactory.create_batch(10, broker=broker_account)

    with CaptureQueriesContext(connection) as query_context:
        response = auth_broker.get("/api/purchasedashboard/")

    assert response.status_code == 200
    breakpoint()
    assert len(query_context) == 6
