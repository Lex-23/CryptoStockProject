from market.models import Market
from rest_framework import serializers


class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = ["id", "name", "url"]
