#  for all api test cases api_client should be authenticated


def test_get_account(first_user_account, auth_first_user):
    response = auth_first_user.get("/api/account/")
    assert response.status_code == 200
    assert response.json() == {
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


def test_get_account_another_user(
    first_user_account, second_user_account, auth_second_user
):
    response = auth_second_user.get("/api/account/")
    assert response.status_code == 200
    assert response.json() == {
        "id": second_user_account.id,
        "name": second_user_account.name,
        "owner": second_user_account.owner.username,
        "cash_balance": "0.0000",
        "wallet": {
            "id": second_user_account.wallet.id,
            "name": second_user_account.wallet.name,
        },
        "wallet_records": [],
    }


def test_get_account_not_authenticated_user(api_client):
    response = api_client.get("/api/account/")
    assert response.status_code == 401
