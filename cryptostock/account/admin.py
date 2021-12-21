from account.models import Broker, Client, Offer, PurchaseDashboard, SalesDashboard
from django.contrib import admin


class SalesDashboardInline(admin.TabularInline):
    model = SalesDashboard
    extra = 1


class OfferInline(admin.TabularInline):
    model = Offer
    extra = 1


class AccountAdmin(admin.ModelAdmin):
    fields = ("owner", "name", "wallet", "cash_balance", "telegram_chat_id")
    search_fields = ("owner__username", "name")
    list_display = ("id", "owner", "name", "wallet", "cash_balance", "telegram_chat_id")
    list_editable = ("cash_balance",)


@admin.register(Client)
class ClientAdmin(AccountAdmin):
    inlines = [OfferInline]


@admin.register(Broker)
class BrokerAdmin(AccountAdmin):
    inlines = [SalesDashboardInline]


@admin.register(SalesDashboard)
class SalesDashboardAdmin(admin.ModelAdmin):
    fields = (
        "asset",
        "count",
        "price",
        "broker",
        "success_offer_notification",
        "count_control_notification",
    )
    list_display = (
        "id",
        "asset",
        "count",
        "price",
        "broker",
        "success_offer_notification",
        "count_control_notification",
    )
    list_editable = ("count", "price")
    search_fields = ("asset__name", "broker__name")
    list_filter = ("asset", "broker")


@admin.register(PurchaseDashboard)
class PurchaseDashboardAdmin(admin.ModelAdmin):
    fields = ("asset", "market", "count", "price", "broker")
    list_display = ("id", "asset", "market", "count", "price", "broker")


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    fields = ("deal", "client", "count")
    list_display = (
        "id",
        "client",
        "asset",
        "price",
        "count",
        "broker",
        "timestamp",
        "total_value",
        "deal_id",
    )
    search_fields = ("client__name", "deal__asset__name", "deal__broker__name")

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
