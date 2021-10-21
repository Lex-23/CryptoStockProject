from account.models import Broker, Client, Offer, SalesDashboard
from django.contrib import admin


class SalesDashboardInline(admin.TabularInline):
    model = SalesDashboard
    extra = 1


class OfferInline(admin.TabularInline):
    model = Offer
    extra = 1


class AccountAdmin(admin.ModelAdmin):
    fields = ("owner", "name", "wallet", "cash_balance")
    search_fields = ("owner", "name")
    list_display = ("id", "owner", "name", "wallet", "cash_balance")
    list_editable = ("cash_balance",)


@admin.register(Client)
class ClientAdmin(AccountAdmin):
    inlines = [OfferInline]


@admin.register(Broker)
class BrokerAdmin(AccountAdmin):
    inlines = [SalesDashboardInline]


@admin.register(SalesDashboard)
class SalesDashboardAdmin(admin.ModelAdmin):
    fields = ("asset", "count", "price", "broker")
    list_display = ("id", "asset", "count", "price", "broker")
    list_editable = ("count", "price")
    ordering = ("asset", "broker")
    search_fields = ("asset", "broker")
    list_filter = ("asset", "broker")


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    fields = ("client", "asset", "count", "price", "broker")
    list_display = (
        "id",
        "client",
        "asset",
        "count",
        "price",
        "broker",
        "timestamp",
        "total_value",
    )
    list_editable = ("count", "price")
    ordering = ("asset", "broker", "client", "timestamp")
    search_fields = ("asset", "broker", "client")
    list_filter = ("asset", "broker")
