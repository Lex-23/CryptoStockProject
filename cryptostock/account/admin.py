from account.models import Broker, Client
from django.contrib import admin


@admin.register(Broker)
class BrokerAdmin(admin.ModelAdmin):
    fields = ("owner", "name", "wallet")
    search_fields = ("owner", "name")
    list_display = ("id", "owner", "name", "wallet")


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    fields = ("owner", "name", "wallet")
    search_fields = ("owner", "name")
    list_display = ("id", "owner", "name", "wallet")
