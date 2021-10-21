from asset.serializers import AssetSerializer
from rest_framework import serializers
from wallet.models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ["id", "name"]


class WalletRecordSerializer(serializers.ModelSerializer):
    assets = AssetSerializer()
    wallet = WalletSerializer()

    class Meta:
        model = Wallet
        fields = ["id", "name", "assets"]
