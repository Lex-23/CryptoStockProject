from account.models import Account, Broker, Client, Offer, SalesDashboard
from asset.models import Asset
from asset.serializers import AssetSerializer
from market.serializers import MarketSerializer
from rest_framework import serializers
from wallet.serializers import WalletRecordSerializer, WalletSerializer


class AccountSerializer(serializers.ModelSerializer):
    wallet = WalletSerializer()
    owner = serializers.StringRelatedField()
    wallet_records = WalletRecordSerializer(many=True)

    class Meta:
        model = Account
        fields = ["id", "name", "owner", "cash_balance", "wallet", "wallet_records"]


class BrokerSerializer(AccountSerializer):
    class Meta:
        model = Broker
        fields = ["id", "name", "owner", "wallet"]


class ClientSerializer(AccountSerializer):
    class Meta:
        model = Client
        fields = ["id", "name", "owner", "wallet"]


class SalesDashboardSerializer(serializers.ModelSerializer):
    broker = BrokerSerializer(required=False)
    asset = AssetSerializer(required=False)

    class Meta:
        model = SalesDashboard
        fields = [
            "id",
            "asset",
            "count",
            "price",
            "broker",
            "success_offer_notification",
            "count_control_notification",
        ]


class PurchaseDashboardSerializer(serializers.ModelSerializer):
    broker = BrokerSerializer()
    asset = AssetSerializer()
    market = MarketSerializer()
    timestamp = serializers.DateTimeField()

    class Meta:
        model = SalesDashboard
        fields = ["id", "asset", "broker", "market", "price", "count", "timestamp"]


class CreateSalesDashboardSerializer(serializers.ModelSerializer):
    queryset = Asset.objects.all()
    asset = serializers.PrimaryKeyRelatedField(queryset=queryset)

    class Meta:
        model = SalesDashboard
        fields = [
            "asset",
            "count",
            "price",
            "success_offer_notification",
            "count_control_notification",
        ]


class OfferSerializer(serializers.ModelSerializer):
    asset = AssetSerializer(required=False)
    client = ClientSerializer(required=False)
    broker = BrokerSerializer(required=False)
    price = serializers.DecimalField(required=False, decimal_places=2, max_digits=16)
    timestamp = serializers.DateTimeField(required=False)
    total_value = serializers.DecimalField(
        required=False, max_digits=30, decimal_places=2
    )

    class Meta:
        model = Offer
        fields = [
            "id",
            "asset",
            "client",
            "count",
            "price",
            "broker",
            "total_value",
            "timestamp",
        ]
