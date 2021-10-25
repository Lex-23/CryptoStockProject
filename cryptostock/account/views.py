from account.models import Offer, SalesDashboard
from account.serializers import (
    AccountSerializer,
    OfferSerializer,
    SalesDashboardSerializer,
)
from asset.models import Asset
from django.db import transaction
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from utils import validators
from utils.services import (
    broker_wallet_record_flow,
    client_wallet_record_flow,
    create_offer,
    create_sale_object,
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
            validators.validate_is_broker(request)
            validators.validate_asset_exists(asset, broker)
            validators.validate_asset_count(request, asset, broker)

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
            validators.validate_is_broker(request)
            validators.validate_broker_owner_sale(request, sale)
            validators.validate_asset_count(request, sale.asset, sale.broker)
            serializer.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        sale = self.get_object(pk)

        validators.validate_is_broker(request)
        validators.validate_broker_owner_sale(request, sale)
        sale.delete()

        return Response({"status": "sale deleted"}, status=status.HTTP_204_NO_CONTENT)


class OffersListApiView(APIView):
    def get_sale(self, pk):
        try:
            return SalesDashboard.objects.get(pk=pk)
        except SalesDashboard.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        offers = Offer.objects.all()
        serializer = OfferSerializer(offers, many=True)
        return Response(serializer.data)

    @transaction.atomic
    def post(self, request, pk, format=None):
        data = request.data
        client = request.user.account.client
        deal = self.get_sale(pk=pk)
        offer_count = {"count": data["count"]}
        serializer = OfferSerializer(data=offer_count)

        if serializer.is_valid():
            offer_count = serializer.data["count"]

            validators.validate_is_client(request)
            validators.validate_offer_count(serializer, deal)

            offer = create_offer(client, deal, count=offer_count)
            deal_value = offer.total_value
            validators.validate_cash_balance(client, deal_value)

            client_wallet_record_flow(client, deal, count=offer_count)
            broker = deal.broker
            broker_wallet_record_flow(broker, deal, count=offer_count)
            validators.update_cash_balance(client, broker, value=deal_value)
            validators.update_deal(deal, count=offer_count)

            offer.save()
            serializer = OfferSerializer(offer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountApiView(APIView):
    def get(self, request, format=None):
        account = request.user.account
        serializer = AccountSerializer(account)
        return Response(serializer.data)
