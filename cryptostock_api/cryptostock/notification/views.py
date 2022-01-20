from notification.models import Consumer, ConsumerType
from notification.serializers import FromTelegramDataSerializer
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from utils.notification_handlers.activate_consumers import (
    CONSUMER_ACTIVATE_DATA,
    join_tg_consumer_with_bot,
)
from utils.validators import validate_consumer_exists, validate_consumer_type


class TelegramNotificationActivateApiView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = FromTelegramDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        join_tg_consumer_with_bot(
            serializer.data["account_token"], serializer.data["chat_id"]
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateConsumerApiView(APIView):
    def post(self, request, consumer_type, **kwargs):
        account = request.user.account
        validate_consumer_type(consumer_type)
        validate_consumer_exists(consumer_type, account)

        Consumer.objects.create(account=account, type=ConsumerType(consumer_type))
        data = CONSUMER_ACTIVATE_DATA[consumer_type](account)
        return Response(data, status=status.HTTP_201_CREATED)
