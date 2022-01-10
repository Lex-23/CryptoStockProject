import pytest
from account.tests.conftest import *  # noqa
from notification.models import ConsumerType


@pytest.fixture(scope="session")
def celery_config():
    return {
        "broker_url": "redis://localhost:6379",
        "result_backend": "redis://localhost:6379",
    }


@pytest.fixture
def tg_notify():
    return "telegram notify is success"


@pytest.fixture
def email_notify():
    return "email notify is success"


SENDER = {ConsumerType.TELEGRAM: tg_notify, ConsumerType.EMAIL: email_notify}
