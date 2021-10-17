from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("account.urls")),
    path("api/v2/", include("market.urls")),
]
