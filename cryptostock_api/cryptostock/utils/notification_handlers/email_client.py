import os

from django.conf import settings
from django.core.mail import send_mail

CRYPTOSTOCK_NAME = os.environ["CRYPTOSTOCK_NAME"]


def email_notify(message, context):
    # TODO: validate context
    recipient = context.get("recipient")
    subject = f"Notification from {CRYPTOSTOCK_NAME}"
    if isinstance(message, dict):
        subject = message["subject"]
        message = message["body"]

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        recipient,
        html_message=message,
        fail_silently=False,
    )
