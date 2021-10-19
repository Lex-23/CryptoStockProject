from asset.serializers import AssetSerializer
from rest_framework import serializers
from wallet.models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    assets = AssetSerializer(many=True)

    class Meta:
        model = Wallet
        fields = ["id", "name", "assets"]
