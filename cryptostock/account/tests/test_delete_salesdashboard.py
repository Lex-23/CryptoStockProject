from account.tests.factory import BrokerFactory, SalesDashboardFactory


def test_delete_sales_dashboard(auth_broker, broker_account):
    sale = SalesDashboardFactory(broker=broker_account)

    response = auth_broker.delete(f"/api/salesdashboard/{sale.id}/")
    response1 = auth_broker.get(f"/api/salesdashboard/{sale.id}/")

    assert response.status_code == 204
    assert response1.status_code == 404
    assert response1.json() == {"detail": "Not found."}


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
