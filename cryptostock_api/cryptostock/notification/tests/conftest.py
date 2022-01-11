from unittest.mock import MagicMock

import pytest
from account.tests.conftest import *  # noqa
from cryptostock import celery_app
from notification.models import ConsumerType


@pytest.fixture(scope="session")
def celery_config():
    return {
        "broker_url": "redis://localhost:6379",
        "result_backend": "redis://localhost:6379",
    }


@pytest.fixture(scope="module")
def celeryapp(request):
    celery_app.conf.update(CELERY_ALWAYS_EAGER=True)
    return celery_app


tg_notify = MagicMock(return_value="success telegram notify")
email_notify = MagicMock(return_value="success email notify")

SENDER = {ConsumerType.TELEGRAM: tg_notify, ConsumerType.EMAIL: email_notify}
