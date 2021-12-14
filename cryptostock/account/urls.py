from account import views
from django.urls import path

urlpatterns = [
    path("salesdashboard/", views.SalesListApiView.as_view()),
    path("salesdashboard/<int:pk>/", views.SaleApiView.as_view()),
    path("salesdashboard/<int:pk>/buy/", views.NewOfferApiView.as_view()),
    path("offer/", views.OffersListApiView.as_view()),
    path("offer/<int:pk>/", views.OfferApiView.as_view()),
    path("account/", views.AccountApiView.as_view()),
    path("purchasedashboard/", views.PurchaseDashboardListApiView.as_view()),
    path("purchasedashboard/<int:pk>/", views.PurchaseDashboardApiView.as_view()),
]
