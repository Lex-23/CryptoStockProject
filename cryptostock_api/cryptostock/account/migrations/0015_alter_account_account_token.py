# Generated by Django 3.2.11 on 2022-01-26 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("account", "0014_account_account_token")]

    operations = [
        migrations.AlterField(
            model_name="account",
            name="account_token",
            field=models.CharField(
                blank=True,
                help_text="for generate using uuid4",
                max_length=32,
                null=True,
                unique=True,
            ),
        )
    ]
