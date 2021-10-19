from django.urls import re_path
from user.views import LoginAPIView, RegistrationAPIView

urlpatterns = [
    re_path("registration/", RegistrationAPIView.as_view(), name="user_registration"),
    re_path("login/", LoginAPIView.as_view(), name="user_login"),
]
