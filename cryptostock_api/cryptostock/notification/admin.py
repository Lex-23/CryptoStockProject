from django.contrib import admin
from notification.models import NotificationType, Notifier


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
