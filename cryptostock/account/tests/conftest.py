import pytest
from account.models import Account
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from wallet.models import Wallet


@pytest.fixture
def first_user(db):
    user = User.objects.create_user(
        "tester1", "tester1@test.com", "SuperStrongPassword1"
    )
    return user


@pytest.fixture
def second_user(db):
    user = User.objects.create_user(
        "tester2", "tester2@test.com", "SuperStrongPassword2"
    )
    return user


@pytest.fixture
def first_user_account(first_user):
    wallet = Wallet.objects.create(name="Test Wallet1")
    account = Account.objects.create(
        owner=first_user, name="Test account1", wallet=wallet
    )
    return account


@pytest.fixture
def second_user_account(second_user):
    wallet = Wallet.objects.create(name="Test Wallet2")
    account = Account.objects.create(
        owner=second_user, name="Test account2", wallet=wallet
    )
    return account


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def auth_first_user(api_client, first_user):
    api_client.force_authenticate(user=first_user)
    return api_client


@pytest.fixture
def auth_second_user(api_client, second_user):
    api_client.force_authenticate(user=second_user)
    return api_client
