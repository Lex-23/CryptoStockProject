from django.contrib import admin
from wallet.models import Wallet, WalletRecord


class WalletRecordInline(admin.TabularInline):
    model = WalletRecord
    extra = 1


@admin.register(WalletRecord)
class WalletRecordAdmin(admin.ModelAdmin):
    fields = ("asset", "count", "wallet")
    search_fields = ("wallet__name", "asset__name", "wallet__account__name")
    list_display = ("id", "asset", "count", "wallet")
    list_filter = ("wallet__account",)


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    inlines = [WalletRecordInline]
    fields = ("name",)
    search_fields = ("name",)
    list_display = ("id", "name")
