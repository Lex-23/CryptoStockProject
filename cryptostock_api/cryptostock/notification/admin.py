from django.contrib import admin
from notification.models import (
    BrokerNotificationSubscription,
    ClientNotificationSubscription,
    Consumer,
)


@admin.register(Consumer)
class ConsumerAdmin(admin.ModelAdmin):
    fields = ("account", "enable", "type", "data")
    list_display = ("id", "account", "enable", "type", "data")


class NotificationSubscriptionAdmin(admin.ModelAdmin):
    fields = ("account", "enable", "notification_type", "data")
    list_display = ("id", "account", "enable", "notification_type", "data")
    list_editable = ("enable",)


@admin.register(BrokerNotificationSubscription)
class BrokerNotificationSubscriptionAdmin(NotificationSubscriptionAdmin):
    pass


@admin.register(ClientNotificationSubscription)
class ClientNotificationSubscriptionAdmin(NotificationSubscriptionAdmin):
    pass
