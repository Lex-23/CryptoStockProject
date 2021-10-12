from asset.models import Asset, AssetType
from django.contrib import admin


@admin.register(AssetType)
class AssetTypeAdmin(admin.ModelAdmin):
    fields = ("name", "description")
    search_fields = ("name",)
    list_display = ("id", "name")


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    fields = ("type", "price", "count")
    search_fields = ("type",)
    list_display = ("id", "type", "price", "count")
    list_editable = ("price", "count")
