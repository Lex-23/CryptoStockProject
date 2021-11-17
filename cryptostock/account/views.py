from account.models import SalesDashboard
from account.serializers import (
    AccountSerializer,
    CreateSalesDashboardSerializer,
    OfferSerializer,
    SalesDashboardSerializer,
)
from django.db import transaction
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from utils import validators
from utils.services import create_sale_object_serializer, get_offers, offer_flow


class SalesListApiView(APIView):
    def get(self, request, format=None):
        sales = SalesDashboard.objects.all()
        serializer = SalesDashboardSerializer(sales, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CreateSalesDashboardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sale_data = create_sale_object_serializer(
            request=request, **serializer.validated_data
        )
        return Response(sale_data, status=status.HTTP_201_CREATED)


class SaleApiView(APIView):
    def get_sales_dashboard(self, pk):
        return get_object_or_404(SalesDashboard, pk=pk)

    def get(self, request, pk, format=None):
        sale = self.get_sales_dashboard(pk)
        serializer = SalesDashboardSerializer(sale)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        sale = self.get_sales_dashboard(pk)
        serializer = SalesDashboardSerializer(sale, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        validators.broker_validate(request, sale)
        data = serializer.validated_data
        if "count" in data:
            validators.validate_asset_count(data["count"], sale.asset, sale.broker)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        sale = self.get_sales_dashboard(pk)
        validators.broker_validate(request, sale)

        sale.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class NewOfferApiView(APIView):
    @transaction.atomic
    def post(self, request, pk, format=None):
        deal = get_object_or_404(SalesDashboard, pk=pk)
        serializer = OfferSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        offer_count = serializer.validated_data["count"]
        offer_data = offer_flow(offer_count, request, deal)
        return Response(offer_data, status=status.HTTP_201_CREATED)


class OffersListApiView(APIView):
    def get(self, request, format=None):
        offers = get_offers(request)
        serializer = OfferSerializer(offers, many=True)
        return Response(serializer.data)


class OfferApiView(APIView):
    def get(self, request, pk, format=None):
        offer = get_object_or_404(get_offers(request), pk=pk)
        serializer = OfferSerializer(offer)
        return Response(serializer.data)


class AccountApiView(APIView):
    def get(self, request, format=None):
        account = request.user.account
        serializer = AccountSerializer(account)
        return Response(serializer.data)
