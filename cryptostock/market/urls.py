from django.urls import path
from market.views import (
    AssetMarketApiView,
    AssetMarketListApiView,
    BuyAssetMarketApiView,
)

urlpatterns = [
    path("market/<str:name>/asset/", AssetMarketListApiView.as_view()),
    path(
        "market/<str:market_name>/asset/<str:asset_name>/", AssetMarketApiView.as_view()
    ),
    path(
        "market/<str:market_name>/asset/<str:asset_name>/buy/",
        BuyAssetMarketApiView.as_view(),
    ),
]
