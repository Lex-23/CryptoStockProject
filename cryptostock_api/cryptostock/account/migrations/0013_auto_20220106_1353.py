# Generated by Django 3.2.8 on 2022-01-06 13:53

from decimal import Decimal

import django.core.validators
import django.db.models.deletion
import utils.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("asset", "0002_alter_asset_description"),
        ("account", "0012_auto_20220106_0812"),
    ]

    operations = [
        migrations.RemoveField(model_name="offer", name="deal"),
        migrations.AddField(
            model_name="offer",
            name="asset",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="asset.asset",
            ),
        ),
        migrations.AddField(
            model_name="offer",
            name="broker",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="account.broker",
            ),
        ),
        migrations.AddField(
            model_name="offer",
            name="price",
            field=utils.fields.PriceField(
                decimal_places=2,
                default=1,
                max_digits=16,
                validators=[django.core.validators.MinValueValidator(Decimal("0.01"))],
            ),
            preserve_default=False,
        ),
    ]
