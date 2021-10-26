from account.views import (
    AccountApiView,
    OffersListApiView,
    SaleApiView,
    SalesListApiView,
)
from django.urls import path

urlpatterns = [
    path("salesdashboard/", SalesListApiView.as_view()),
    path("salesdashboard/<int:pk>/", SaleApiView.as_view()),
    path("newsale/<int:pk>/", SaleApiView.as_view()),
    path("offers/", OffersListApiView.as_view()),
    path("offers/<int:pk>/", OffersListApiView.as_view()),
    path("account/", AccountApiView.as_view()),
]
