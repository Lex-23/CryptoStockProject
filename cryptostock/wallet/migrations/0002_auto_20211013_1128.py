# Generated by Django 3.2.8 on 2021-10-13 11:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("asset", "0001_initial"), ("wallet", "0001_initial")]

    operations = [
        migrations.RemoveField(model_name="wallet", name="asset"),
        migrations.CreateModel(
            name="WalletAssistant",
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
                ("date_joined", models.DateField(auto_now=True)),
                (
                    "asset",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="asset.asset"
                    ),
                ),
                (
                    "wallet",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="wallet.wallet"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="wallet",
            name="assets",
            field=models.ManyToManyField(
                through="wallet.WalletAssistant", to="asset.Asset"
            ),
        ),
    ]
