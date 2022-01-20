from django.urls import path
from notification.views import (
    CreateConsumerApiView,
    TelegramNotificationActivateApiView,
)

urlpatterns = [
    path("tg_notify-on", TelegramNotificationActivateApiView.as_view()),
    path(
        "notifications/create_consumer/<str:consumer_type>/",
        CreateConsumerApiView.as_view(),
    ),
]
