from account.tests.factory import SalesDashboardFactory
from django.db import connection
from django.test.utils import CaptureQueriesContext


def test_get_sales_dashboard(auth_user, broker_account):
    sale = SalesDashboardFactory(broker=broker_account)

    response = auth_user.get(f"/api/salesdashboard/{sale.id}/")

    assert response.status_code == 200
    assert response.json() == {
        "id": sale.id,
        "asset": {
            "id": sale.asset.id,
            "name": sale.asset.name,
            "description": sale.asset.description,
        },
        "count": f"{sale.count}",
        "price": f"{sale.price}",
        "broker": {
            "id": sale.broker.id,
            "name": sale.broker.name,
            "owner": sale.broker.owner.username,
            "wallet": {"id": sale.broker.wallet.id, "name": sale.broker.wallet.name},
        },
        "success_offer_notification": sale.success_offer_notification,
        "count_control_notification": f"{sale.count_control_notification}",
    }


def test_get_sales_dashboard_db_calls(auth_user, broker_account):
    sale = SalesDashboardFactory(broker=broker_account)

    with CaptureQueriesContext(connection) as query_context:
        response = auth_user.get(f"/api/salesdashboard/{sale.id}/")

    assert response.status_code == 200
    assert len(query_context) == 2


def test_get_sales_dashboard_not_authenticated_user(api_client, broker_account):
    sale = SalesDashboardFactory(broker=broker_account)
    response = api_client.get(f"/api/salesdashboard/{sale.id}/")

    assert response.status_code == 401
