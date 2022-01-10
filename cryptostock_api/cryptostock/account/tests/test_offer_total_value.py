import decimal

import pytest
from account.tests.factory import OfferFactory, SalesDashboardFactory


@pytest.mark.parametrize(
    "count,price,expected_total_value",
    [
        ("10", "10", decimal.Decimal("100")),
        ("5.5555", "5.55", decimal.Decimal("30.84")),
        ("0.5555", "1", decimal.Decimal("0.56")),
        ("0.0001", "1", decimal.Decimal("0.01")),
        ("0.0001", "0.01", decimal.Decimal("0.01")),
        (
            "9999999999.0001",
            "9999999999.01",
            decimal.Decimal("99999999980101000000.99"),
        ),
    ],
)
def test_offer_total_value(count, price, expected_total_value):
    deal = SalesDashboardFactory(
        count=decimal.Decimal("1000.0000"), price=decimal.Decimal(price)
    )
    offer = OfferFactory(
        asset=deal.asset,
        broker=deal.broker,
        price=deal.price,
        count=decimal.Decimal(count),
    )
    assert offer.total_value == expected_total_value
