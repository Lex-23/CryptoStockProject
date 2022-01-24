from notification.models import Consumer


def test_create_email_consumer(broker_account, auth_broker):
    expected_data = {"recipient": "test@mail.com"}
    response = auth_broker.post(
        "/api/notifications/consumers/EMAIL/", data=expected_data
    )
    expected_consumer = Consumer.objects.get(type="EMAIL", account=broker_account)

    assert response.status_code == 201
    assert expected_consumer.data["recipient"] == [expected_data["recipient"]]
