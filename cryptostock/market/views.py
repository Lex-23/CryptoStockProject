from market.models import Market
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
    def get(self, request, format=None, **kwargs):
        validate_is_broker(request)
        market = get_object_or_404(
            queryset=Market.objects.all(), name=kwargs["market_name"]
        )
        asset = market.client.get_asset(name=kwargs["asset_name"])
        if asset is None:
            raise ValidationError(
                [
                    f"asset {kwargs['asset_name']} not allow for market {kwargs['market_name']}."
                ]
            )
        return Response(asset)
