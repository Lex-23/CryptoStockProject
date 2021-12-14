from account.models import SalesDashboard
from account.serializers import (
    AccountSerializer,
    CreateSalesDashboardSerializer,
    OfferSerializer,
    PurchaseDashboardSerializer,
    SalesDashboardSerializer,
)
from django.db import transaction
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from utils import validators
from utils.services import (
    create_sale_object_serializer,
    get_offers_with_related_items,
    get_purchasedashboards_with_related_items,
    offer_flow,
)
from utils.validators import validate_is_broker


class SalesListApiView(APIView, LimitOffsetPagination):
    def get(self, request, format=None):
        sales = (
            SalesDashboard.objects.select_related(
                "asset", "broker__owner", "broker__wallet"
            )
            .prefetch_related("asset__wallet_record")
            .all()
        )
        results = self.paginate_queryset(sales, request, view=self)
        serializer = SalesDashboardSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = CreateSalesDashboardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sale_data = create_sale_object_serializer(
            request=request, **serializer.validated_data
        )
        return Response(sale_data, status=status.HTTP_201_CREATED)


class SaleApiView(APIView):
    def get_sales_dashboard(self, pk):
        return get_object_or_404(
            queryset=SalesDashboard.objects.select_related(
                "asset", "broker__owner", "broker__wallet"
            )
            .prefetch_related("asset__wallet_record")
            .all(),
            pk=pk,
        )

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
        sale = get_object_or_404(
            queryset=SalesDashboard.objects.select_related(
                "broker__owner", "broker__wallet", "asset"
            ).all(),
            pk=pk,
        )
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


class OffersListApiView(APIView, LimitOffsetPagination):
    def get_queryset(self):
        return get_offers_with_related_items(self.request)

    def get(self, request, format=None):
        results = self.paginate_queryset(self.get_queryset(), request, view=self)
        serializer = OfferSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)


class OfferApiView(APIView):
    def get_queryset(self):
        return get_offers_with_related_items(self.request)

    def get(self, request, pk, format=None):
        offer = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = OfferSerializer(offer)
        return Response(serializer.data)


class AccountApiView(APIView):
    def get(self, request, format=None):
        account = request.user.account
        serializer = AccountSerializer(account)
        return Response(serializer.data)


class PurchaseDashboardListApiView(APIView, LimitOffsetPagination):
    def get_queryset(self):
        return get_purchasedashboards_with_related_items(self.request)

    def get(self, request, format=None):
        validate_is_broker(request)
        results = self.paginate_queryset(self.get_queryset(), request, view=self)
        serializer = PurchaseDashboardSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)


class PurchaseDashboardApiView(APIView):
    def get_queryset(self):
        return get_purchasedashboards_with_related_items(self.request)

    def get(self, request, pk, format=None):
        validate_is_broker(request)
        purchase = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = PurchaseDashboardSerializer(purchase)
        return Response(serializer.data)
