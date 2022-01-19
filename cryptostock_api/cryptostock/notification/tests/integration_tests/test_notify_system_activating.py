import uuid


def test_post_activate_turn_on(api_client):
    response = api_client.post("/api/notify-on", data={"chat_id": 1})
    breakpoint()

    assert response.status_code == 200
    assert response.json() == {"chat_id": "1"}


def test_success_create_consumer(auth_broker, broker_account):
    broker_account.account_token = uuid.uuid4().hex
    join_url = f"https://t.me/cryptostock_2021_bot?start={broker_account.account_token}"
    breakpoint()
    response = auth_broker.post(
        "/api/notifications/create_consumer/", data={"join_url": join_url}
    )
    breakpoint()

    assert response.status_code == 200
    assert response.json() == {"join_url": join_url}
