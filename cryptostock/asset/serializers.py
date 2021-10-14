from asset.models import Asset
from rest_framework import serializers


class AssetSerializer(serializers.ModelSerializer):
    type = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Asset
        fields = ["id", "type", "price", "count"]
