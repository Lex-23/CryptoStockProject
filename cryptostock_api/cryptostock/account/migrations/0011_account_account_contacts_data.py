# Generated by Django 3.2.8 on 2021-12-27 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "account",
            "0010_remove_account_telegram_chat_id_squashed_0011_alter_salesdashboard_broker",
        )
    ]

    operations = [
        migrations.AddField(
            model_name="account",
            name="account_contacts_data",
            field=models.JSONField(
                default=dict,
                help_text="all contact data about account. Such as telegram id, email and other.",
            ),
        )
    ]
