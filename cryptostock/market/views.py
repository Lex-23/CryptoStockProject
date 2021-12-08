from market.models import Market
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from utils.validators import validate_is_broker


class AssetBuySerializer(serializers.ModelSerializer):
    count = serializers.IntegerField()


class AssetMarketListApiView(APIView):
    def get(self, request, name, format=None):
        validate_is_broker(request)
        market = get_object_or_404(queryset=Market.objects.all(), name=name)
        return Response(market.client.get_assets())


class AssetMarketApiView(APIView):
    def get(self, request, market_name, asset_name, format=None):
        validate_is_broker(request)
        market = get_object_or_404(queryset=Market.objects.all(), name=market_name)
        asset = market.client.get_asset(name=asset_name)
        if asset is None:
            raise ValidationError(
                [f"asset {asset_name} not allow for market {market_name}."]
            )
        return Response(asset)


class BuyAssetMarketApiView(APIView):
    def post(self, request, market_name, asset_name, format=None):
        validate_is_broker(request)
        count = request.data["count"]
        AssetBuySerializer(data=count).is_valid(raise_exception=True)
        market = get_object_or_404(queryset=Market.objects.all(), name=market_name)
        return Response(market.client.buy(name=asset_name, count=count))
