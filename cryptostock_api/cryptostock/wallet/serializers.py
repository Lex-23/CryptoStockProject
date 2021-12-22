from asset.serializers import AssetSerializer
from rest_framework import serializers
from wallet.models import Wallet, WalletRecord


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ["id", "name"]


class WalletRecordSerializer(serializers.ModelSerializer):
    asset = AssetSerializer()

    class Meta:
        model = WalletRecord
        fields = ["id", "asset", "count"]
