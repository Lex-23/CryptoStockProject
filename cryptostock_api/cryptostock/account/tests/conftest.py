import decimal

import pytest
from account.models import Broker, Client
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from utils.jwt_views import MyTokenObtainPairSerializer
from wallet.models import Wallet

TEST_USERS_PASSWORDS = {
    "user": "SuperStrongPassword",
    "user_one": "SuperStrongPassword1",
    "user_two": "SuperStrongPassword2",
}


@pytest.fixture
def user(db):
    user = User.objects.create_user(
        "tester", "tester@test.com", TEST_USERS_PASSWORDS["user"]
    )
    return user


@pytest.fixture
def user_one(db):
    user = User.objects.create_user(
        "tester1", "tester1@test.com", TEST_USERS_PASSWORDS["user_one"]
    )
    return user


@pytest.fixture
def user_two(db):
    user = User.objects.create_user(
        "tester2", "tester2@test.com", TEST_USERS_PASSWORDS["user_two"]
    )
    return user


@pytest.fixture
def account_factory():
    def create_account(user, wallet_name, account_name, user_model, **kwargs):
        # 'user_model' is the django model: Broker or Client
        wallet = Wallet.objects.create(name=wallet_name)
        account = user_model.objects.create(
            owner=user, name=account_name, wallet=wallet, **kwargs
        )
        return account

    return create_account


@pytest.fixture(autouse=True)
def user_account(account_factory, user):
    """Simulate simple new user, who just now registered in app"""
    return account_factory(
        user=user,
        wallet_name="Test empty wallet",
        account_name="Test account",
        user_model=Client,
    )


@pytest.fixture(autouse=True)
def broker_account(account_factory, user_one):
    return account_factory(
        user=user_one,
        wallet_name="Test Wallet broker",
        account_name="Test account broker",
        user_model=Broker,
        cash_balance=decimal.Decimal("1000.00"),
    )


@pytest.fixture(autouse=True)
def client_account(account_factory, user_two):
    return account_factory(
        user=user_two,
        wallet_name="Test Wallet client",
        account_name="Test account client",
        user_model=Client,
        cash_balance=decimal.Decimal("10000.00"),
    )


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def auth_user(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def auth_factory(db, api_client):
    def auth_user(user):
        token = MyTokenObtainPairSerializer.get_token(user)
        access = token.access_token
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        return api_client

    return auth_user


@pytest.fixture
def auth_broker(auth_factory, user_one):
    return auth_factory(user=user_one)


@pytest.fixture
def auth_client(auth_factory, user_two):
    return auth_factory(user=user_two)
