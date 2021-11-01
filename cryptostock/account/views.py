from account.models import Offer, SalesDashboard
from account.serializers import (
    AccountSerializer,
    OfferSerializer,
    SalesDashboardSerializer,
)
from asset.models import Asset
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from utils import validators
from utils.services import create_sale_object_serializer, get_object, offer_flow


class SalesListApiView(APIView):
    def get(self, request, format=None):
        sales = SalesDashboard.objects.all()
        serializer = SalesDashboardSerializer(sales, many=True)
        breakpoint()
        return Response(serializer.data)


class SaleApiView(APIView):
    def get_sale(self, pk):
        return get_object(SalesDashboard, pk)

    def get_asset(self, pk):
        return get_object(Asset, pk)

    def get(self, request, pk, format=None):
        sale = self.get_sale(pk)
        serializer = SalesDashboardSerializer(sale)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        asset = self.get_asset(pk=pk)
        serializer = SalesDashboardSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        count, price = serializer.data["count"], serializer.data["price"]
        sale_data = create_sale_object_serializer(count, price, asset, request)
        return Response(sale_data, status=status.HTTP_201_CREATED)

    def patch(self, request, pk, format=None):
        sale = self.get_sale(pk)
        serializer = SalesDashboardSerializer(sale, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        validators.broker_validate(request, sale)

        if "count" in request.data:
            validators.validate_asset_count(
                request.data["count"], sale.asset, sale.broker
            )
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        sale = self.get_sale(pk)
        validators.broker_validate(request.user.account, sale)
        sale.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OffersListApiView(APIView):
    def get_sale(self, pk):
        return get_object(SalesDashboard, pk)

    def get(self, request, format=None):
        offers = Offer.objects.all()
        serializer = OfferSerializer(offers, many=True)
        return Response(serializer.data)

    @transaction.atomic
    def post(self, request, pk, format=None):
        deal = self.get_sale(pk=pk)
        serializer = OfferSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        offer_count = serializer.data["count"]
        offer_data = offer_flow(offer_count, request, deal)
        return Response(offer_data, status=status.HTTP_201_CREATED)


class AccountApiView(APIView):
    def get(self, request, format=None):
        account = request.user.account
        serializer = AccountSerializer(account)
        return Response(serializer.data)
