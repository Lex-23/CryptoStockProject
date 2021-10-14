from account.views import DetailBroker, DetailClient, ListBrokers, ListClients
from django.urls import path
from market.views import ListMarkets

urlpatterns = [
    path("markets/", ListMarkets.as_view()),
    path("brokers/", ListBrokers.as_view()),
    path("brokers/<pk>/", DetailBroker.as_view()),
    path("clients/", ListClients.as_view()),
    path("clients/<pk>/", DetailClient.as_view()),
]
