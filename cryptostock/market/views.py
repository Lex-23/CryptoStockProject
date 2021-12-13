from django.db import transaction
from market.models import Market
from market.serializers import AssetBuySerializer
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from utils.services import purchase_asset
from utils.validators import get_validated_asset_from_market, validate_is_broker


class AssetMarketListApiView(APIView):
    def get(self, request, name, format=None):
        validate_is_broker(request)
        market = get_object_or_404(queryset=Market.objects.all(), name=name)
        return Response(market.client.get_assets())


class AssetMarketApiView(APIView):
    def get(self, request, market_name, asset_name, format=None):
        validate_is_broker(request)
        market = get_object_or_404(queryset=Market.objects.all(), name=market_name)
        asset = get_validated_asset_from_market(asset_name, market)
        return Response(asset)


class BuyAssetMarketApiView(APIView):
    @transaction.atomic
    def post(self, request, market_name, asset_name, format=None):
        validate_is_broker(request)
        serializer = AssetBuySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        market = get_object_or_404(queryset=Market.objects.all(), name=market_name)
        deal = purchase_asset(
            request, market, asset_name, count=serializer.data["count"]
        )
        return Response(deal, status=status.HTTP_201_CREATED)
