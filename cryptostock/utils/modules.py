import decimal

from django.core.validators import MinValueValidator
from django.db import models


class CustomDecimalField(models.DecimalField):
    """default field for price in Auctions"""

    MAX_DIGITS = 20
    DECIMAL_PLACES = 6
    VALIDATORS = [MinValueValidator(decimal.Decimal("0.000001"))]

    def __init__(self, **kwargs):
        kwargs.setdefault("max_digits", self.MAX_DIGITS)
        kwargs.setdefault("decimal_places", self.DECIMAL_PLACES)
        kwargs.setdefault("validators", self.VALIDATORS)
        super().__init__(**kwargs)
