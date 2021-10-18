# Generated by Django 3.2.8 on 2021-10-18 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("asset", "0001_initial"), ("wallet", "0003_alter_wallet_assets")]

    operations = [
        migrations.AlterField(
            model_name="wallet",
            name="assets",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="wallet",
                through="wallet.WalletAssistant",
                to="asset.Asset",
            ),
        )
    ]
