from account.models import Broker, Client
from account.serializers import AssetBuySerializer, BrokerSerializer, ClientSerializer
from asset.models import Asset
from asset.serializers import AssetSerializer
from django.http import Http404
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from utils.validators import (
    validate_account,
    validate_price_positive,
    validate_price_type,
    validate_wallet,
)


class ListBrokers(APIView):
    def get(self, request):
        queryset = Broker.objects.all()
        serializer = BrokerSerializer(queryset, many=True)
        return Response(serializer.data)


class BrokerDetailAssets(APIView):
    def get_object(self, pk):
        try:
            return Broker.objects.get(pk=pk)
        except Broker.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        broker = self.get_object(pk)
        serializer = BrokerSerializer(broker)
        return Response(serializer.data["wallet"]["assets"])


class AssetDetail(APIView):
    def get_queryset(self):
        queryset = Asset.objects.all()
        return queryset

    def get(self, request, *args, **kwargs):
        asset = get_object_or_404(self.get_queryset(), pk=kwargs["pk"])
        serializer = AssetSerializer(asset)

        validate_wallet(asset, kwargs["wal_id"])
        validate_account(asset, kwargs["acc_id"])
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        asset = get_object_or_404(self.get_queryset(), pk=kwargs["pk"])
        data = request.data
        asset.price = data.get("price", asset.price)

        validate_price_type(asset)
        validate_price_positive(asset)

        asset.save()
        serializer = AssetSerializer(asset)

        validate_wallet(asset, kwargs["wal_id"])
        validate_account(asset, kwargs["acc_id"])
        return Response(serializer.data)


class ListClients(APIView):
    def get(self, request):
        queryset = Client.objects.all()
        serializer = BrokerSerializer(queryset, many=True)
        if serializer.is_valid():
            return Response(serializer.data)


class DetailClient(APIView):
    def get(self, request, pk=None):
        queryset = Client.objects.all()
        client = get_object_or_404(queryset, pk=pk)
        serializer = ClientSerializer(client)
        return Response(serializer.data)


class BuyAsset(APIView):
    def post(self, request, *args, **kwargs):
        assets = Asset.objects.all()
        asset = get_object_or_404(assets, pk=kwargs["pk"])
        serializer = AssetBuySerializer(data=request.data)

        if serializer.is_valid():
            validate_wallet(asset, kwargs["wal_id"])
            validate_account(asset, kwargs["acc_id"])
