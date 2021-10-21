from asset.models import Asset
from django.contrib import admin


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    fields = ("name", "description")
    search_fields = ("name",)
    list_display = ("name", "id", "description")
