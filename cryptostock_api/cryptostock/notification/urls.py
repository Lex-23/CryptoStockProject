from django.urls import path
from notification.views import (
    CreateConsumerApiView,
    TelegramNotificationActivateApiView,
    VKNotificationActivateApiView,
)

urlpatterns = [
    path(
        "notifications/consumers/<str:consumer_type>/", CreateConsumerApiView.as_view()
    ),
    path(
        "notifications/consumers/TELEGRAM/activate/",
        TelegramNotificationActivateApiView.as_view(),
    ),
    path(
        "notifications/consumers/VK/activate/", VKNotificationActivateApiView.as_view()
    ),
]
