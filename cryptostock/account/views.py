from account.models import Broker, Client
from account.serializers import BrokerSerializer, ClientSerializer
from asset.models import Asset
from asset.serializers import AssetSerializer
from django.http import Http404
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from wallet.serializers import WalletSerializer


class ListBrokers(APIView):
    def get(self, request):
        queryset = Broker.objects.all()
        serializer = BrokerSerializer(queryset, many=True)
        return Response(serializer.data)


class BrokerAssets(APIView):
    def get(self, request, pk=None):
        queryset = Broker.objects.all()
        broker = get_object_or_404(queryset, pk=pk)
        wallet = broker.wallet
        serializer = WalletSerializer(wallet)
        return Response(serializer.data["assets"])


class AssetDetail(APIView):
    def get(self, request, pk=None):
        queryset = Asset.objects.all()
        asset = get_object_or_404(queryset, pk=pk)
        serializer = AssetSerializer(asset)
        return Response(serializer.data)


class ListClients(APIView):
    def get(self, request):
        queryset = Client.objects.all()
        serializer = BrokerSerializer(queryset, many=True)
        return Response(serializer.data)


class DetailClient(APIView):
    def get(self, request, pk=None):
        queryset = Client.objects.all()
        client = get_object_or_404(queryset, pk=pk)
        serializer = ClientSerializer(client)
        return Response(serializer.data)


class BrokersAPIView(APIView):
    serializer_class = BrokerSerializer

    def get_queryset(self):
        brokers = Broker.objects.all()
        return brokers


class BrokerDetail(APIView):
    def get_object(self, pk):
        try:
            return Broker.objects.get(pk=pk)
        except Broker.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        broker = self.get_object(pk)
        serializer = BrokerSerializer(broker)
        return Response(serializer.data)
