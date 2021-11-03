from account.views import (
    AccountApiView,
    OfferApiView,
    OffersListApiView,
    SaleApiView,
    SalesListApiView,
)
from django.urls import path

urlpatterns = [
    path("salesdashboard/", SalesListApiView.as_view()),
    path("salesdashboard/<int:pk>/", SaleApiView.as_view()),
    path("salesdashboard/<int:pk>/buy/", OffersListApiView.as_view()),
    path("offers/", OffersListApiView.as_view()),
    path("offers/<int:pk>/", OfferApiView.as_view()),
    path("account/", AccountApiView.as_view()),
]
