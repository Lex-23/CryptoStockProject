# Generated by Django 3.2.8 on 2021-12-21 15:55

from decimal import Decimal

import django.core.validators
import utils.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("account", "0008_auto_20211217_1513")]

    operations = [
        migrations.AddField(
            model_name="account",
            name="telegram_chat_id",
            field=models.BigIntegerField(
                blank=True,
                help_text="input here 'chat_id' from telegram_bot https://t.me/cryptostock_2021_bot",
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="salesdashboard",
            name="count_control_notification",
            field=utils.fields.CountField(
                decimal_places=4,
                default=Decimal("1"),
                help_text="input here min count, after which you want get notification (on default = 1).",
                max_digits=14,
                validators=[
                    django.core.validators.MinValueValidator(Decimal("0.0001"))
                ],
            ),
        ),
    ]