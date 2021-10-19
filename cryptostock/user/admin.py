from django.contrib import admin
from user.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ("username", "email", "is_staff", "is_superuser", "is_active")
    search_fields = ("username", "email")
    list_display = ("id", "username", "email", "is_staff", "is_superuser", "is_active")
