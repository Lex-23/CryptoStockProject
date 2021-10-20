from account.views import (
    AssetDetail,
    BrokerDetailAssets,
    BuyAsset,
    DetailClient,
    ListBrokers,
    ListClients,
)
from django.urls import path

urlpatterns = [
    path("brokers/", ListBrokers.as_view()),
    path("brokers/<pk>/assets/", BrokerDetailAssets.as_view()),
    path(
        "brokers/<int:acc_id>/wallet/<int:wal_id>/asset/<int:pk>/",
        AssetDetail.as_view(),
    ),
    path("clients/", ListClients.as_view()),
    path("clients/<pk>/", DetailClient.as_view()),
    path(
        "brokers/<int:acc_id>/wallet/<int:wal_id>/asset/<int:pk>/buy/",
        BuyAsset.as_view(),
    ),
]
