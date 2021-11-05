def test_get_self_account(first_user_account, auth_client1):
    response = (auth_client1.get("/api/account/")).json()
    assert response["id"] == first_user_account.id


def test_data_get_self_account(first_user_account, auth_client1):
    response = (auth_client1.get("/api/account/")).json()
    actual_data = {
        "id": first_user_account.id,
        "name": first_user_account.name,
        "owner": first_user_account.owner.username,
        "cash_balance": "0.0000",
        "wallet": {
            "id": first_user_account.wallet.id,
            "name": first_user_account.wallet.name,
        },
        "wallet_records": [],
    }
    assert actual_data == response
    assert 0 == first_user_account.cash_balance


def test_user_not_get_another_account(
    first_user_account, second_user_account, auth_client2
):
    response = (auth_client2.get("/api/account/")).json()
    assert response["id"] != first_user_account.id
    assert response["id"] == second_user_account.id
