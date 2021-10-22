from account.views import SaleApiView, SalesListApiView
from django.urls import path

urlpatterns = [
    path("salesdashboard/", SalesListApiView.as_view()),
    path("salesdashboard/<int:pk>/", SaleApiView.as_view()),
    path("salesdashboard/<int:pk>/update/", SaleApiView.as_view()),
    path("salesdashboard/<int:pk>/delete/", SaleApiView.as_view()),
    path("newsale/<int:pk>/", SalesListApiView.as_view()),
]
