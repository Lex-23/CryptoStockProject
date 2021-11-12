from account.tests.factory import SalesDashboardFactory


def test_delete_sales_dashboard(auth_broker, broker_account):
    sale = SalesDashboardFactory(broker=broker_account)

    response = auth_broker.delete(f"/api/salesdashboard/{sale.id}/")
    response1 = auth_broker.get(f"/api/salesdashboard/{sale.id}/")

    assert response.status_code == 204
    assert response1.status_code == 404
    assert response1.json() == {"detail": "Not found."}
