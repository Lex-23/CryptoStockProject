from account.tests.conftest import TEST_USERS_PASSWORDS
from utils.jwt_views import MyTokenObtainPairSerializer


def test_jwt_auth(user_one, auth_broker):
    data = {"username": user_one.username, "password": TEST_USERS_PASSWORDS["user_one"]}
    auth_broker.logout()

    response = auth_broker.post("/api/auth/", data=data)
    token = MyTokenObtainPairSerializer.get_token(user_one)

    assert response.status_code == 200
    assert "refresh" in response.json().keys() and "access" in response.json().keys()
    assert token["user_role"] == "broker"


def test_jwt_auth_refresh(user_two, auth_client):
    data = {"username": user_two.username, "password": TEST_USERS_PASSWORDS["user_two"]}
    auth_client.logout()

    token_obtain_pair = (auth_client.post("/api/auth/", data=data)).json()
    token = MyTokenObtainPairSerializer.get_token(user_two)
    refresh_token = token_obtain_pair["refresh"]
    data["refresh"] = refresh_token

    response = auth_client.post("/api/auth/refresh/", data=data)

    assert response.status_code == 200
    assert "refresh" in response.json().keys() and "access" in response.json().keys()
    assert token["user_role"] == "client"
    assert response.json()["access"] != token_obtain_pair["access"]
    assert response.json()["refresh"] != token_obtain_pair["refresh"]


def test_jwt_auth_not_exists_user(api_client):
    data = {"username": "RandomName", "password": "RandomPassword"}

    response = api_client.post("/api/auth/", data=data)

    assert response.status_code == 401
    assert response.json() == {
        "detail": "No active account found with the given credentials"
    }
