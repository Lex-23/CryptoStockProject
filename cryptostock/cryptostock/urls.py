from django.contrib import admin
from django.urls import include, path
from utils import jwt_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("account.urls")),
    path("api/", include("market.urls")),
    path(
        "api/auth/", jwt_views.MyTokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path(
        "api/auth/refresh/",
        jwt_views.MyTokenObtainPairView.as_view(),
        name="token_refresh",
    ),
]
