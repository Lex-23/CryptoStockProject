from django.contrib import admin
from wallet.models import Wallet


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    fields = ("asset", "name")
    search_fields = ("name",)
    list_display = ("id", "name", "get_assets")

    def get_assets(self, obj):
        return "\n".join([str(_) for _ in obj.asset.all()])
