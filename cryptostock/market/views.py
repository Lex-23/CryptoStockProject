from market.models import Market
from market.serializers import MarketSerializer
from rest_framework.viewsets import ModelViewSet


class MarketViewSet(ModelViewSet):
    queryset = Market.objects.all()
    serializer_class = MarketSerializer
