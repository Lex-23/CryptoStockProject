import pytest
from account.models import Broker, Client
from asset.models import Asset
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from utils.jwt_views import MyTokenObtainPairSerializer
from wallet.models import Wallet, WalletRecord


@pytest.fixture
def user(db):
    user = User.objects.create_user("tester", "tester@test.com", "SuperStrongPassword")
    return user


@pytest.fixture
def user_one(db):
    user = User.objects.create_user(
        "tester1", "tester1@test.com", "SuperStrongPassword1"
    )
    return user


@pytest.fixture
def user_two(db):
    user = User.objects.create_user(
        "tester2", "tester2@test.com", "SuperStrongPassword2"
    )
    return user


@pytest.fixture
def account_factory(db):
    def create_broker(user, wallet_name, account_name, user_model):
        # 'user_model' is the django model: Broker or Client
        wallet = Wallet.objects.create(name=wallet_name)
        broker = user_model.objects.create(owner=user, name=account_name, wallet=wallet)
        return broker

    return create_broker


@pytest.fixture
def asset_factory(db):
    def create_asset(name, description="asset description"):
        asset = Asset.objects.create(name=name, description=description)
        return asset

    return create_asset


@pytest.fixture
def wallet_record_factory(db):
    def create_wallet_record(asset, account, count):
        wallet = account.wallet
        wallet_record = WalletRecord.objects.create(
            asset=asset, wallet=wallet, count=count
        )
        return wallet_record

    return create_wallet_record


@pytest.fixture
def user_account(account_factory, user):
    return account_factory(
        user=user,
        wallet_name="Test empty wallet",
        account_name="Test account",
        user_model=Client,
    )


@pytest.fixture
def broker_account(account_factory, user_one):
    return account_factory(
        user=user_one,
        wallet_name="Test Wallet broker",
        account_name="Test account broker",
        user_model=Broker,
    )


@pytest.fixture(autouse=True)
def client_account(account_factory, user_two):
    return account_factory(
        user=user_two,
        wallet_name="Test Wallet client",
        account_name="Test account client",
        user_model=Client,
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


@pytest.fixture
def asset_btc(asset_factory):
    return asset_factory(name="BTC")


@pytest.fixture
def asset_eth(asset_factory):
    return asset_factory(name="ETH")


@pytest.fixture(autouse=True)
def wallet_record_one_broker(
    wallet_record_factory, asset_btc, broker_account, count=500
):
    return wallet_record_factory(asset=asset_btc, account=broker_account, count=count)
