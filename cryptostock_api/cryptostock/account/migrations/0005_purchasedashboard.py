# Generated by Django 3.2.8 on 2021-12-09 14:23

from decimal import Decimal

import django.core.validators
import django.db.models.deletion
import utils.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("market", "0002_auto_20211206_1257"),
        ("asset", "0001_initial"),
        ("account", "0004_auto_20211122_1300"),
    ]

    operations = [
        migrations.CreateModel(
            name="PurchaseDashboard",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "price",
                    utils.fields.PriceField(
                        decimal_places=6,
                        max_digits=16,
                        validators=[
                            django.core.validators.MinValueValidator(
                                Decimal("0.000001")
                            )
                        ],
                    ),
                ),
                (
                    "count",
                    utils.fields.CountField(
                        decimal_places=4,
                        default=0,
                        max_digits=14,
                        validators=[
                            django.core.validators.MinValueValidator(Decimal("0.0001"))
                        ],
                    ),
                ),
                (
                    "asset",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING, to="asset.asset"
                    ),
                ),
                (
                    "broker",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="account.broker"
                    ),
                ),
                (
                    "market",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="market.market",
                    ),
                ),
            ],
        )
    ]
