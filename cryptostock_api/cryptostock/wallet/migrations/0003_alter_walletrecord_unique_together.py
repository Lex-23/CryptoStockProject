# Generated by Django 3.2.8 on 2021-10-21 15:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("asset", "0001_initial"), ("wallet", "0002_walletrecord")]

    operations = [
        migrations.AlterUniqueTogether(
            name="walletrecord", unique_together={("asset", "wallet")}
        )
    ]
