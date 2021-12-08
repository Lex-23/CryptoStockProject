from django.urls import path
from market.views import AssetMarketApiView, AssetMarketListApiView

urlpatterns = [
    path("market/<str:name>/asset/", AssetMarketListApiView.as_view()),
    path(
        "market/<str:market_name>/asset/<str:asset_name>/", AssetMarketApiView.as_view()
    ),
]
