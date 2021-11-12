import pytest
from account.models import SalesDashboard
from account.tests.factory import BrokerFactory, SalesDashboardFactory
from django.http.response import Http404
from rest_framework.generics import get_object_or_404


def test_delete_sales_dashboard(auth_broker, broker_account):
    sale = SalesDashboardFactory(broker=broker_account)

    response = auth_broker.delete(f"/api/salesdashboard/{sale.id}/")
    with pytest.raises(Http404) as exc:
        get_object_or_404(SalesDashboard.objects.all(), id=sale.id)

    assert response.status_code == 204
    assert exc.type == Http404
    assert "No SalesDashboard matches the given query." in str(exc.value)


def test_delete_sales_dashboard_not_broker(auth_client, broker_account):
    sale = SalesDashboardFactory(broker=broker_account)

    response = auth_client.delete(f"/api/salesdashboard/{sale.id}/")

    assert response.status_code == 400
    assert response.json() == [
        "You are not a broker. You haven`t permissions for this operation."
    ]


def test_update_not_own_sales_dashboard(auth_broker):
    another_broker = BrokerFactory()
    sale = SalesDashboardFactory(broker=another_broker)

    response = auth_broker.delete(f"/api/salesdashboard/{sale.id}/")

    assert response.status_code == 400
    assert response.json() == [
        "You haven`t permissions for this operation. This is not your sale."
    ]
