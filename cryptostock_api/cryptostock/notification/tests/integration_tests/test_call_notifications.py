import decimal as d
from unittest.mock import patch

import pytest
from account.models import SalesDashboard
from account.tests.factory import (
    BrokerFactory,
    SalesDashboardFactory,
    WalletRecordFactory,
)


@pytest.mark.parametrize(
    "is_available_notification,function_called", [(True, True), (False, False)]
)
@patch(
    "utils.api_view_assistants.async_notify_success_offer",
    return_value="success notify",
)
def test_async_notify_success_offer(
    async_notify_success_offer, auth_client, is_available_notification, function_called
):
    broker = BrokerFactory()
    wallet_record = WalletRecordFactory(wallet=broker.wallet, count=d.Decimal("150.00"))
    sale = SalesDashboardFactory(
        asset=wallet_record.asset,
        broker=broker,
        success_offer_notification=is_available_notification,
    )

    response = auth_client.post(
        f"/api/salesdashboard/{sale.id}/buy/", data={"count": "2"}
    )

    assert response.status_code == 201
    assert async_notify_success_offer.called is function_called


@pytest.mark.parametrize(
    "offer_count,function_called", [("30", True), ("31", True), ("29", False)]
)
@patch(
    "utils.api_view_assistants.async_notify_salesdashboard_soon_over",
    return_value="success notify",
)
def test_async_notify_salesdashboard_soon_over(
    async_notify_salesdashboard_soon_over, auth_client, offer_count, function_called
):
    broker = BrokerFactory()
    wallet_record = WalletRecordFactory(wallet=broker.wallet, count=d.Decimal("50.00"))
    sale = SalesDashboardFactory(
        asset=wallet_record.asset,
        broker=broker,
        count=d.Decimal("50.00"),
        count_control_notification=d.Decimal("20.00"),
    )
    data = {"count": offer_count}

    response = auth_client.post(f"/api/salesdashboard/{sale.id}/buy/", data)
    assert response.status_code == 201
    assert async_notify_salesdashboard_soon_over.called is function_called


@pytest.mark.parametrize("offer_count,function_called", [("30", True), ("29", False)])
@patch(
    "utils.api_view_assistants.async_notify_salesdashboard_is_over",
    return_value="success notify",
)
def test_async_notify_salesdashboard_is_over(
    async_notify_salesdashboard_is_over, auth_client, offer_count, function_called
):
    broker = BrokerFactory()
    wallet_record = WalletRecordFactory(wallet=broker.wallet, count=d.Decimal("50.00"))
    sale = SalesDashboardFactory(
        asset=wallet_record.asset,
        broker=broker,
        count=d.Decimal("30.00"),
        count_control_notification=d.Decimal("20.00"),
    )

    data = {"count": offer_count}

    response = auth_client.post(f"/api/salesdashboard/{sale.id}/buy/", data)

    assert response.status_code == 201
    assert async_notify_salesdashboard_is_over.called is function_called


@patch(
    "utils.api_view_assistants.async_notify_salesdashboard_is_over",
    return_value="success notify",
)
def test_deleting_salesdashboard_after_it_has_been_over(
    async_notify_salesdashboard_is_over, auth_client
):
    broker = BrokerFactory()
    wallet_record = WalletRecordFactory(wallet=broker.wallet, count=d.Decimal("50.00"))
    sale = SalesDashboardFactory(
        asset=wallet_record.asset, broker=broker, count=d.Decimal("30.00")
    )

    response = auth_client.post(
        f"/api/salesdashboard/{sale.id}/buy/", {"count": sale.count}
    )

    assert response.status_code == 201
    assert async_notify_salesdashboard_is_over.called is True
    with pytest.raises(
        SalesDashboard.DoesNotExist,
        match="SalesDashboard matching query does not exist.",
    ):
        SalesDashboard.objects.get(id=sale.id)
