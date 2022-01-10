import decimal as d

import pytest
from account.tests.factory import (
    BrokerFactory,
    SalesDashboardFactory,
    WalletRecordFactory,
)
from django.db import connection
from django.test.utils import CaptureQueriesContext


@pytest.mark.parametrize(
    "data",
    [
        ({"count": "615.0000", "price": "250.48"}),
        ({"count": "700.4558"}),
        ({"price": "525.45"}),
    ],
)
def test_update_sales_dashboard(auth_broker, broker_account, data):
    wallet_record = WalletRecordFactory(
        wallet=broker_account.wallet, count=d.Decimal("1000.0000")
    )
    asset = wallet_record.asset
    sale = SalesDashboardFactory(
        broker=broker_account,
        asset=wallet_record.asset,
        count=d.Decimal("500.0000"),
        price=d.Decimal("345.54"),
    )
    asset_count_before_update = broker_account.wallet.wallet_record.get(
        asset=asset
    ).count

    response = auth_broker.patch(f"/api/salesdashboard/{sale.pk}/", data=data)
    asset_count_after_update = broker_account.wallet.wallet_record.get(
        asset=asset
    ).count

    assert response.status_code == 200
    assert asset_count_after_update == asset_count_before_update
    assert response.json() == {
        "id": sale.id,
        "asset": {
            "id": sale.asset.id,
            "name": sale.asset.name,
            "description": sale.asset.description,
        },
        "count": data.get("count", f"{sale.count}"),
        "price": data.get("price", f"{sale.price}"),
        "broker": {
            "id": sale.broker.id,
            "name": sale.broker.name,
            "owner": sale.broker.owner.username,
            "wallet": {"id": sale.broker.wallet.id, "name": sale.broker.wallet.name},
        },
        "success_offer_notification": sale.success_offer_notification,
        "count_control_notification": f"{sale.count_control_notification}",
    }


@pytest.mark.parametrize(
    "data,query_count",
    [
        ({"count": "615.0000", "price": "250.48"}, 7),
        ({"count": "700.4558"}, 7),
        ({"price": "525.45"}, 6),
    ],
)
def test_update_sales_dashboard_db_calls(
    auth_broker, broker_account, data, query_count
):
    wallet_record = WalletRecordFactory(
        wallet=broker_account.wallet, count=d.Decimal("1000.0000")
    )
    sale = SalesDashboardFactory(
        broker=broker_account,
        asset=wallet_record.asset,
        count=d.Decimal("500.0000"),
        price=d.Decimal("345.54"),
    )

    with CaptureQueriesContext(connection) as query_context:
        response = auth_broker.patch(f"/api/salesdashboard/{sale.pk}/", data=data)

    assert response.status_code == 200
    assert len(query_context) == query_count


def test_update_sales_dashboard_not_broker(auth_client, broker_account):
    wallet_record = WalletRecordFactory(
        wallet=broker_account.wallet, count=d.Decimal("1000.0000")
    )
    asset = wallet_record.asset
    sale = SalesDashboardFactory(
        broker=broker_account,
        asset=asset,
        count=d.Decimal("500.0000"),
        price=d.Decimal("345.54"),
    )
    data = {"price": "452.00"}

    response = auth_client.patch(f"/api/salesdashboard/{sale.pk}/", data=data)

    assert response.status_code == 400
    assert response.json() == [
        "You are not a broker. You haven`t permissions for this operation."
    ]


def test_update_not_own_sales_dashboard(auth_broker):
    another_broker = BrokerFactory()
    wallet_record = WalletRecordFactory(
        wallet=another_broker.wallet, count=d.Decimal("1000.0000")
    )
    asset = wallet_record.asset
    sale = SalesDashboardFactory(
        broker=another_broker,
        asset=asset,
        count=d.Decimal("500.0000"),
        price=d.Decimal("345.54"),
    )
    data = {"price": "452.00"}

    response = auth_broker.patch(f"/api/salesdashboard/{sale.pk}/", data=data)

    assert response.status_code == 400
    assert response.json() == [
        "You haven`t permissions for this operation. This is not your sale."
    ]


def test_update_sales_dashboard_count_too_much(auth_broker, broker_account):
    wallet_record = WalletRecordFactory(
        wallet=broker_account.wallet, count=d.Decimal("1000.0000")
    )
    asset = wallet_record.asset
    sale = SalesDashboardFactory(
        broker=broker_account,
        asset=asset,
        count=d.Decimal("500.0000"),
        price=d.Decimal("345.54"),
    )
    data = {"count": "1000.0001"}

    response = auth_broker.patch(f"/api/salesdashboard/{sale.pk}/", data=data)

    assert response.status_code == 400
    assert response.json() == [f"You haven`t that much {asset.name}."]
