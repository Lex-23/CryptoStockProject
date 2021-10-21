from account.models import Broker, Client, SalesDashboard
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


class SalesDashboardSerializer(serializers.ModelSerializer):
    broker = BrokerSerializer()
    asset = AssetSerializer()

    class Meta:
        model = SalesDashboard
        fields = ["id", "asset", "count", "price", "broker"]


class OfferSerializer(serializers.ModelSerializer):
    deal = SalesDashboardSerializer()
    client = ClientSerializer()

    class Meta:
        model = SalesDashboard
        fields = ["id", "asset", "broker", "total_value", "timestamp", "deal"]
