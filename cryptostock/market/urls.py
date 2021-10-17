from django.urls import path
from market.views import ListMarkets

urlpatterns = [path("markets/", ListMarkets.as_view())]
