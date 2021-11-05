#  for all api test cases api_client should be authenticated


def test_get_data_self_account(first_user_account, auth_first_user):
    response = auth_first_user.get("/api/account/")
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
    assert actual_data == response.json()
    assert 0 == first_user_account.cash_balance


def test_user_not_get_another_account(
    first_user_account, second_user_account, auth_second_user
):
    response = auth_second_user.get("/api/account/")
    actual_data = {
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
    assert actual_data == response.json()
