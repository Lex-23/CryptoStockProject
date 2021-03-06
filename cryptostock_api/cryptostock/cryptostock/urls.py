import debug_toolbar
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path, re_path
from utils import jwt_views
from utils.jwt_views import AuthTestView
from utils.swagger_views import schema_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("account.urls")),
    path("api/", include("market.urls")),
    path("api/", include("notification.urls")),
    path(
        "api/auth/", jwt_views.MyTokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path(
        "api/auth/refresh/",
        jwt_views.MyTokenObtainPairView.as_view(),
        name="token_refresh",
    ),
    path("api/auth-ping/", AuthTestView.as_view(), name="auth-test"),
    path("__debug__/", include(debug_toolbar.urls)),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(),
        name="schema-json",
    ),
    path("swagger/", schema_view.with_ui("swagger"), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc"), name="schema-redoc"),
    path("health-check/", include("health_check.urls")),
]

urlpatterns += staticfiles_urlpatterns()
