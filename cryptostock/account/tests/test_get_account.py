from django.db import connection
from django.test.utils import CaptureQueriesContext


def test_get_account_new_user(user_account, auth_user):
    #  for api test client should be authenticated
    with CaptureQueriesContext(connection) as query_context:
        response = auth_user.get("/api/account/")
    assert response.status_code == 200
    assert len(query_context) == 1
    assert response.json() == {
        "id": user_account.id,
        "name": user_account.name,
        "owner": user_account.owner.username,
        "cash_balance": f"{user_account.cash_balance}.0000",
        "wallet": {"id": user_account.wallet.id, "name": user_account.wallet.name},
        "wallet_records": [],
    }


def test_get_account_not_authenticated_user(api_client):
    response = api_client.get("/api/account/")
    assert response.status_code == 401
