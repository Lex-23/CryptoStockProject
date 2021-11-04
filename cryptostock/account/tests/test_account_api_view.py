import pytest
from account.models import Account
from django.contrib.auth.models import User
from django.urls import reverse
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
def auth_client1(first_user):
    client = APIClient()
    client.force_authenticate(user=first_user)
    return client


@pytest.fixture
def get_request1(auth_client1):
    client = auth_client1
    response = client.get(reverse("self_account"))
    account_data = response.json()
    return account_data


def test_get_self_account(first_user_account, get_request1):
    response = get_request1
    assert first_user_account.id == response["id"]


def test_data_get_self_account(first_user_account, get_request1):
    response = get_request1
    assert first_user_account.id == response["id"]
    assert first_user_account.owner.username == response["owner"]
    assert first_user_account.name == response["name"]
    assert first_user_account.wallet.id == response["wallet"]["id"]
    assert first_user_account.cash_balance == 0


@pytest.fixture
def auth_client2(second_user):
    client = APIClient()
    client.force_authenticate(user=second_user)
    return client


@pytest.fixture
def get_request2(auth_client2):
    client = auth_client2
    response = client.get(reverse("self_account"))
    account_data = response.json()
    return account_data


def test_user_not_get_another_account(
    first_user_account, second_user_account, get_request2
):
    response = get_request2
    assert response["id"] != first_user_account.id
    assert response["id"] == second_user_account.id
