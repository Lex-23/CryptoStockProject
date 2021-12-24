from account.models import Broker, Client, Offer, PurchaseDashboard, SalesDashboard
from django.contrib import admin
from notification.models import Notifier


class SalesDashboardInline(admin.TabularInline):
    model = SalesDashboard
    extra = 1
    list_per_page = 10


class OfferInline(admin.TabularInline):
    model = Offer
    extra = 1


class NotifierInline(admin.TabularInline):
    model = Notifier
    extra = 1


class AccountAdmin(admin.ModelAdmin):
    fields = ("owner", "name", "wallet", "cash_balance")
    search_fields = ("owner__username", "name")
    list_display = ("id", "owner", "name", "wallet", "cash_balance")
    list_editable = ("cash_balance",)


@admin.register(Client)
class ClientAdmin(AccountAdmin):
    inlines = [OfferInline, NotifierInline]


@admin.register(Broker)
class BrokerAdmin(AccountAdmin):
    inlines = [SalesDashboardInline, NotifierInline]


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
    list_editable = (
        "count",
        "price",
        "success_offer_notification",
        "count_control_notification",
    )
    search_fields = ("asset__name", "broker__name")
    list_filter = ("asset", "broker")
    ordering = ("id", "asset")
    list_per_page = 10


@admin.register(PurchaseDashboard)
class PurchaseDashboardAdmin(admin.ModelAdmin):
    fields = ("asset", "market", "count", "price", "broker")
    list_display = ("id", "asset", "market", "count", "price", "broker")
    list_per_page = 10
    ordering = ("id", "asset")


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
    list_per_page = 10
    ordering = ("id", "deal__asset")

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
