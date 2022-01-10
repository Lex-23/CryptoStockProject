import pytest
from celery_tasks.broker_notification_tasks import mul


@pytest.mark.celery(result_backend="redis://localhost:6379")
def test_celery_raw_fixtures():
    assert mul.delay(4, 4).get(timeout=10) == 16
