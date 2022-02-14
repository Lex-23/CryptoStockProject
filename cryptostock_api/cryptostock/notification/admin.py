from django.contrib import admin
from notification.models import Consumer, NotificationSubscription


@admin.register(Consumer)
class ConsumerAdmin(admin.ModelAdmin):
    fields = ("account", "enable", "type", "data")
    list_display = ("id", "account", "enable", "type", "data")


@admin.register(NotificationSubscription)
class NotificationSubscriptionAdmin(admin.ModelAdmin):
    fields = ("account", "enable", "notification_type", "data")
    list_display = ("id", "account", "enable", "notification_type", "data")
