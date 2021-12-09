from rest_framework import serializers


class AssetBuySerializer(serializers.Serializer):
    count = serializers.IntegerField(min_value=1, max_value=1000000000)
