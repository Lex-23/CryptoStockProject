from account.models import SalesDashboard
from account.serializers import SalesDashboardSerializer
from asset.models import Asset
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from utils.validators import (
    create_sale_object,
    validate_asset_count,
    validate_asset_exists,
    validate_broker_owner_sale,
    validate_is_broker,
    validate_price_positive,
)


class SalesListApiView(APIView):
    def get_asset(self, pk):
        try:
            return Asset.objects.get(pk=pk)
        except Asset.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        sales = SalesDashboard.objects.all()
        serializer = SalesDashboardSerializer(sales, many=True)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        data = request.data
        broker = request.user.account.broker
        asset = self.get_asset(pk=pk)
        new_sale = {"price": data["price"], "count": data["count"]}
        serializer = SalesDashboardSerializer(data=new_sale)

        if serializer.is_valid():

            validate_price_positive(request)
            validate_is_broker(request)
            validate_asset_exists(asset, broker)
            validate_asset_count(request, asset, broker)

            new_object = create_sale_object(serializer, asset, broker)
            return Response(new_object, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SaleApiView(APIView):
    def get_object(self, pk):
        try:
            return SalesDashboard.objects.get(pk=pk)
        except SalesDashboard.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        sale = self.get_object(pk)
        serializer = SalesDashboardSerializer(sale)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        sale = self.get_object(pk)
        serializer = SalesDashboardSerializer(sale, data=request.data)
        if serializer.is_valid():
            breakpoint()
            validate_price_positive(request)
            validate_is_broker(request)
            validate_broker_owner_sale(request, sale)
            validate_asset_count(request, sale.asset, sale.broker)
            serializer.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        sale = self.get_object(pk)

        validate_is_broker(request)
        validate_broker_owner_sale(request, sale)
        sale.delete()

        return Response({"status": "sale deleted"}, status=status.HTTP_204_NO_CONTENT)
