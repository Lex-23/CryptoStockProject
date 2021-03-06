# Generated by Django 3.2.8 on 2021-11-16 16:08

from decimal import Decimal

import django.core.validators
import utils.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("account", "0002_auto_20211021_1200")]

    operations = [
        migrations.AlterField(
            model_name="account",
            name="cash_balance",
            field=utils.fields.CountField(
                decimal_places=4,
                default=0,
                max_digits=30,
                validators=[
                    django.core.validators.MinValueValidator(Decimal("0.0001"))
                ],
            ),
        ),
        migrations.AlterField(
            model_name="offer",
            name="count",
            field=utils.fields.CountField(
                decimal_places=4,
                default=0,
                max_digits=14,
                validators=[
                    django.core.validators.MinValueValidator(Decimal("0.0001"))
                ],
            ),
        ),
        migrations.AlterField(
            model_name="salesdashboard",
            name="count",
            field=utils.fields.CountField(
                decimal_places=4,
                default=0,
                max_digits=14,
                validators=[
                    django.core.validators.MinValueValidator(Decimal("0.0001"))
                ],
            ),
        ),
        migrations.AlterField(
            model_name="salesdashboard",
            name="price",
            field=utils.fields.PriceField(
                decimal_places=6,
                max_digits=16,
                validators=[
                    django.core.validators.MinValueValidator(Decimal("0.000001"))
                ],
            ),
        ),
    ]
