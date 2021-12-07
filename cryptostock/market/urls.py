from django.urls import path
from market.views import AssetMarketListApiView

urlpatterns = [path("market/<str:name>/asset/", AssetMarketListApiView.as_view())]
