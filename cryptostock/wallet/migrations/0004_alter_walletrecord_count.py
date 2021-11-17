# Generated by Django 3.2.8 on 2021-11-16 16:08

from decimal import Decimal

import django.core.validators
import utils.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("wallet", "0003_alter_walletrecord_unique_together")]

    operations = [
        migrations.AlterField(
            model_name="walletrecord",
            name="count",
            field=utils.fields.CountField(
                decimal_places=4,
                default=0,
                max_digits=14,
                validators=[
                    django.core.validators.MinValueValidator(Decimal("0.0001"))
                ],
            ),
        )
    ]