# Generated by Django 3.2.8 on 2021-12-14 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "account",
            "0006_alter_account_cash_balance_squashed_0008_alter_purchasedashboard_count",
        )
    ]

    operations = [
        migrations.AddField(
            model_name="purchasedashboard",
            name="timestamp",
            field=models.DateTimeField(auto_now=True),
        )
    ]
