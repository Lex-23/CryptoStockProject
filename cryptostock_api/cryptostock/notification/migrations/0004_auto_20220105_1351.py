# Generated by Django 3.2.8 on 2022-01-05 13:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("notification", "0003_auto_20220104_0825")]

    operations = [
        migrations.AlterUniqueTogether(name="notifier", unique_together=None),
        migrations.RemoveField(model_name="notifier", name="account"),
        migrations.RemoveField(model_name="notifier", name="type"),
        migrations.DeleteModel(name="NotificationType"),
        migrations.DeleteModel(name="Notifier"),
    ]