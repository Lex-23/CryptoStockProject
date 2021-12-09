import decimal

from django.core.validators import MinValueValidator
from django.db import models


class PriceField(models.DecimalField):
    """default field for price"""

    MAX_DIGITS = 16
    DECIMAL_PLACES = 2
    VALIDATORS = [MinValueValidator(decimal.Decimal("0.01"))]

    def __init__(self, **kwargs):
        kwargs.setdefault("max_digits", self.MAX_DIGITS)
        kwargs.setdefault("decimal_places", self.DECIMAL_PLACES)
        kwargs.setdefault("validators", self.VALIDATORS)
        super().__init__(**kwargs)


class CountField(models.DecimalField):
    """default field for count asset"""

    MAX_DIGITS = 14
    DECIMAL_PLACES = 4
    VALIDATORS = [MinValueValidator(decimal.Decimal("0.0001"))]
    DEFAULT = 0

    def __init__(self, **kwargs):
        kwargs.setdefault("max_digits", self.MAX_DIGITS)
        kwargs.setdefault("decimal_places", self.DECIMAL_PLACES)
        kwargs.setdefault("validators", self.VALIDATORS)
        kwargs.setdefault("default", self.DEFAULT)
        super().__init__(**kwargs)
