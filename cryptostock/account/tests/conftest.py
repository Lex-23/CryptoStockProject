import pytest
from account.models import Account
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from wallet.models import Wallet


@pytest.fixture
def user(db):
    user = User.objects.create_user("tester", "tester@test.com", "SuperStrongPassword")
    return user


@pytest.fixture
def user_account(user):
    wallet = Wallet.objects.create(name="Test Wallet")
    account = Account.objects.create(owner=user, name="Test account", wallet=wallet)
    return account


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def auth_user(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client
