from django.urls import path
from notification.views import CreateConsumerApiView, NotificationActivateApiView

urlpatterns = [
    path("notify-on", NotificationActivateApiView.as_view()),
    path("notifications/create_consumer/", CreateConsumerApiView.as_view()),
]
