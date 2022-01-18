import logging
from urllib.parse import urlparse

from django.conf import settings

logging.basicConfig(level=logging.INFO)

NOTIFY_ON_URL_PATH = urlparse(settings.NOTIFY_ON_URL).path


class NotificationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path_info == NOTIFY_ON_URL_PATH:
            breakpoint()
            logging.info(f"chat_id: {request.GET.get('id')}")
            return self.get_response(request)

        response = self.get_response(request)
        return response
