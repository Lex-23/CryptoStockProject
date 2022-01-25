import pytest
from django.db import connection
from django.test.utils import CaptureQueriesContext
from notification.models import Consumer
from utils.notification_handlers.activate_consumers import (
    TELEGRAM_BOT_NAME,
    VK_BOT_NUMBER,
)


def test_create_email_consumer(broker_account, auth_broker):
    expected_data = {"recipient": "test@mail.com"}
    response = auth_broker.post(
        "/api/notifications/consumers/EMAIL/", data=expected_data
    )
    expected_consumer = Consumer.objects.get(type="EMAIL", account=broker_account)

    assert response.status_code == 201
    assert response.json() == expected_data["recipient"]
    assert expected_consumer.data["recipient"] == [expected_data["recipient"]]


@pytest.mark.parametrize(
    "consumer_type,join_url_pattern",
    [
        ("TELEGRAM", f"https://t.me/{TELEGRAM_BOT_NAME}?start="),
        ("VK", f"https://vk.com/im?sel=-{VK_BOT_NUMBER}&ref="),
    ],
)
def test_create_vc_and_tg_consumer(
    broker_account, auth_broker, consumer_type, join_url_pattern
):

    response = auth_broker.post(f"/api/notifications/consumers/{consumer_type}/")
    expected_consumer = Consumer.objects.get(type=consumer_type, account=broker_account)

    assert response.status_code == 201
    assert response.json() == {
        "join_url": f"{join_url_pattern}{expected_consumer.account.account_token}"
    }


@pytest.mark.parametrize(
    "consumer_type,post_data,expected_count_queries",
    [
        ("TELEGRAM", None, 7),
        ("VK", None, 7),
        ("EMAIL", {"recipient": "test@mail.com"}, 8),
    ],
)
def test_create_consumers_db_calls(
    auth_broker, consumer_type, post_data, expected_count_queries
):
    with CaptureQueriesContext(connection) as query_context:
        response = auth_broker.post(
            f"/api/notifications/consumers/{consumer_type}/", data=post_data
        )

    assert response.status_code == 201
    assert len(query_context) == expected_count_queries


@pytest.mark.parametrize(
    "consumer_type,post_data",
    [("TELEGRAM", None), ("VK", None), ("EMAIL", {"recipient": "test@mail.com"})],
)
def test_create_consumer_not_authenticated_user(api_client, consumer_type, post_data):
    response = api_client.get(
        f"/api/notifications/consumers/{consumer_type}/", data=post_data
    )
    assert response.status_code == 401
