from account.models import PurchaseDashboard
from asset.models import Asset
from market.models import Market
from market.serializers import AssetBuySerializer
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from utils.validators import validate_is_broker


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

        serializer = AssetBuySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        market = get_object_or_404(queryset=Market.objects.all(), name=market_name)
        deal = market.client.buy(name=asset_name, count=serializer.data["count"])
        breakpoint()
        asset = deal["asset"]
        try:
            Asset.objects.get(name=asset["name"])
        except Asset.DoesNotExist:
            Asset.objects.create(name=asset["name"], description=asset["description"])
        purchase = PurchaseDashboard.objects.create(
            asset=Asset.objects.get(name=asset["name"]),
            market=market,
            broker=request.user.account.broker,
            count=deal["count"],
            price=deal["asset"]["price"],
        )
        broker = request.user.account.broker
        broker.cash_balance -= deal["total_price"]
        broker.save()
        broker_wallet_record = broker.wallet.wallet_record.get(asset=purchase.asset)
        broker_wallet_record.count += purchase.count
        broker_wallet_record.save()
        return Response(deal)
