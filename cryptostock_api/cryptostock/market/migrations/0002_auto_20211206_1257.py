# Generated by Django 3.2.8 on 2021-12-06 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("market", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="market", name="kwargs", field=models.JSONField(default=dict)
        ),
        migrations.AlterField(
            model_name="market",
            name="name",
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
