from django.contrib import admin
from market.models import Market


@admin.register(Market)
class MarketAdmin(admin.ModelAdmin):
    fields = ("name", "url")
    search_fields = ("name",)
    list_display = ("id", "name", "url")
