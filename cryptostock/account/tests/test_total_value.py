import decimal

import pytest
from account.tests.factory import OfferFactory, SalesDashboardFactory


@pytest.mark.parametrize(
    "count,price,expected_total_value",
    [
        ("10", "10", decimal.Decimal("100")),
        ("5.5555", "5.555555", decimal.Decimal("30.8639")),
        ("1", "0.555555", decimal.Decimal("0.5556")),
        ("1", "0.000001", decimal.Decimal("0.0001")),
        ("0.0001", "0.000001", decimal.Decimal("0.0001")),
        (
            "9999999999.0001",
            "9999999999.000001",
            decimal.Decimal("99999999980001010000.9999"),
        ),
    ],
)
def test_offer_total_value(count, price, expected_total_value):
    deal = SalesDashboardFactory(
        count=decimal.Decimal("1000.0000"), price=decimal.Decimal(price)
    )
    offer = OfferFactory(deal=deal, count=decimal.Decimal(count))
    assert offer.total_value == expected_total_value
