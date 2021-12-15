from market.models import Market
from rest_framework import serializers


class AssetBuySerializer(serializers.Serializer):
    count = serializers.IntegerField(min_value=1, max_value=1000000000)


class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = ["id", "name", "url"]
