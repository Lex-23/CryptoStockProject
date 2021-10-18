from account.models import AssetBuy, Broker, Client
from asset.serializers import AssetSerializer
from rest_framework import serializers
from wallet.serializers import WalletSerializer


class AccountSerializer(serializers.ModelSerializer):
    wallet = WalletSerializer()
    owner = serializers.StringRelatedField()


class BrokerSerializer(AccountSerializer):
    class Meta:
        model = Broker
        fields = ["id", "name", "owner", "wallet"]


class ClientSerializer(AccountSerializer):
    class Meta:
        model = Client
        fields = ["id", "name", "owner", "wallet"]


class AssetBuySerializer(serializers.ModelSerializer):
    client = ClientSerializer()
    asset = AssetSerializer()

    class Meta:
        model = AssetBuy
        fields = ["id", "client", "asset", "buy_count", "timestamp"]
