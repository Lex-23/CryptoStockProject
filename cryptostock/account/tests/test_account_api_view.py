def test_get_account(user_account, auth_user):
    #  for api test client should be authenticated
    response = auth_user.get("/api/account/")
    assert response.status_code == 200
    assert response.json() == {
        "id": user_account.id,
        "name": user_account.name,
        "owner": user_account.owner.username,
        "cash_balance": "0.0000",
        "wallet": {"id": user_account.wallet.id, "name": user_account.wallet.name},
        "wallet_records": [],
    }


def test_get_account_not_authenticated_user(api_client):
    response = api_client.get("/api/account/")
    assert response.status_code == 401
