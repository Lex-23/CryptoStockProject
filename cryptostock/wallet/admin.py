from django.contrib import admin
from wallet.models import Wallet, WalletAssistant


class WalletAssistantInline(admin.TabularInline):
    model = WalletAssistant
    extra = 1


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    inlines = (WalletAssistantInline,)
    fields = ("name",)
    search_fields = ("name",)
    list_display = ("id", "name")
