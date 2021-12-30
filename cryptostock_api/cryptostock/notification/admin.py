from django.contrib import admin
from notification.models import (
    Consumer,
    NotificationSubscription,
    NotificationType,
    Notifier,
)


@admin.register(NotificationType)
class NotificationTypeAdmin(admin.ModelAdmin):
    fields = ("name",)
    list_display = ("id", "name")


@admin.register(Notifier)
class NotifierAdmin(admin.ModelAdmin):
    fields = ("account", "type", "active")
    list_display = ("id", "account", "type", "active")
    list_editable = ("active",)
    list_filter = ("account", "type")


@admin.register(Consumer)
class ConsumerAdmin(admin.ModelAdmin):
    fields = ("account", "enable", "type", "data")
    list_display = ("id", "account", "enable", "type", "data")


@admin.register(NotificationSubscription)
class NotificationSubscriptionAdmin(admin.ModelAdmin):
    fields = ("account", "enable", "notification_type")
    list_display = ("id", "account", "enable", "notification_type")
