from django.urls import path
from user.views import LoginAPIView, RegistrationAPIView

urlpatterns = [
    path("registration/", RegistrationAPIView.as_view(), name="user_registration"),
    path("login/", LoginAPIView.as_view(), name="user_login"),
]
