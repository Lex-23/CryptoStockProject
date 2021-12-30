from django.conf.global_settings import EMAIL_HOST_USER
from django.core.mail import send_mail


def email_notify(subject, message, recipient, **kwargs):
    send_mail(subject, message, EMAIL_HOST_USER, recipient, fail_silently=False)
