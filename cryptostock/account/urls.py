from account.views import (
    AccountApiView,
    NewOfferApiView,
    OfferApiView,
    OffersListApiView,
    PurchaseDashboardListApiView,
    SaleApiView,
    SalesListApiView,
)
from django.urls import path

urlpatterns = [
    path("salesdashboard/", SalesListApiView.as_view()),
    path("salesdashboard/<int:pk>/", SaleApiView.as_view()),
    path("salesdashboard/<int:pk>/buy/", NewOfferApiView.as_view()),
    path("offer/", OffersListApiView.as_view()),
    path("offer/<int:pk>/", OfferApiView.as_view()),
    path("account/", AccountApiView.as_view()),
    path("purchasedashboard/", PurchaseDashboardListApiView.as_view()),
]
