from account.models import Account
from celery_tasks.general_notification_tasks import success_notification_activated
from django.db import transaction
from notification.models import Consumer, ConsumerType
from notification.serializers import (
    CreateConsumerSerializer,
    FromTelegramDataSerializer,
    FromVKDataSerializer,
)
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from utils.notification_handlers.activate_consumers import (
    CONSUMER_ACTIVATE_DATA,
    join_tg_consumer_with_bot,
    join_vk_consumer_with_bot,
)
from utils.validators import validate_consumer_exists, validate_consumer_type


class TelegramNotificationActivateApiView(APIView):
    permission_classes = [permissions.AllowAny]

    @transaction.atomic
    def post(self, request):
        serializer = FromTelegramDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account = Account.objects.get(account_token=serializer.data["account_token"])

        join_tg_consumer_with_bot(account, serializer.data["chat_id"])
        success_notification_activated.s(account.id, "TELEGRAM").apply_async(
            task_id=f"telegram consumer ON - account: {account.id}"
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class VKNotificationActivateApiView(APIView):
    permission_classes = [permissions.AllowAny]

    @transaction.atomic
    def post(self, request):
        serializer = FromVKDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account = Account.objects.get(account_token=serializer.data["account_token"])

        join_vk_consumer_with_bot(account, serializer.data["peer_id"])
        success_notification_activated.s(account.id, "VK").apply_async(
            task_id=f"vk consumer ON - account: {account.id}"
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateConsumerApiView(APIView):
    @transaction.atomic
    def post(self, request, consumer_type):
        account = request.user.account
        validate_consumer_type(consumer_type)
        validate_consumer_exists(consumer_type, account)

        Consumer.objects.create(account=account, type=ConsumerType(consumer_type))
        serializer = CreateConsumerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = CONSUMER_ACTIVATE_DATA[consumer_type](account, **serializer.data)
        return Response(data, status=status.HTTP_201_CREATED)
