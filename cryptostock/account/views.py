from account.models import Broker, Client
from account.serializers import BrokerSerializer, ClientSerializer
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView


class ListBrokers(APIView):
    def get(self, request):
        brokers = Broker.objects.all()
        serializer = BrokerSerializer(brokers, many=True)
        return Response(serializer.data)


class DetailBroker(APIView):
    def get(self, request, pk=None):
        brokers = Broker.objects.all()
        broker = get_object_or_404(brokers, pk=pk)
        serializer = BrokerSerializer(broker)
        return Response(serializer.data)


class ListClients(APIView):
    def get(self, request):
        clients = Client.objects.all()
        serializer = BrokerSerializer(clients, many=True)
        return Response(serializer.data)


class DetailClient(APIView):
    def get(self, request, pk=None):
        clients = Client.objects.all()
        client = get_object_or_404(clients, pk=pk)
        serializer = ClientSerializer(client)
        return Response(serializer.data)
