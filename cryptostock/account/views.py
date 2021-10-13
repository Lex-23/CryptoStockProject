from account.models import Broker, Client
from account.serializers import BrokerSerializer, ClientSerializer
from rest_framework.viewsets import ModelViewSet


class BrokerViewSet(ModelViewSet):
    queryset = Broker.objects.all()
    serializer_class = BrokerSerializer


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
