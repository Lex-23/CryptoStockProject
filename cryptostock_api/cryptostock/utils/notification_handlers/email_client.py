from django.conf.global_settings import EMAIL_HOST_USER
from django.core.mail import send_mail


def email_notify(**kwargs):
    send_mail(
        kwargs["subject"],
        kwargs["message"],
        EMAIL_HOST_USER,
        kwargs["recipient"],
        fail_silently=False,
    )
