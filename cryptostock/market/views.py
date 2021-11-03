from market.models import Market
from market.serializers import MarketSerializer
from rest_framework.response import Response
from rest_framework.views import APIView


class ListMarkets(APIView):
    def get(self, request):
        clients = Market.objects.all()
        serializer = MarketSerializer(clients, many=True)
        return Response(serializer.data)
