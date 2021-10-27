from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("account.urls")),
    path("api/", include("market.urls")),
    path(
        "api/auth/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path(
        "api/auth/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"
    ),
]
