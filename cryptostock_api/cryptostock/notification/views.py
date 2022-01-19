import uuid

from account.models import Account
from notification.models import Consumer, ConsumerType
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView


class NotificationActivateApiView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        chat_id_info = request.data
        account_token = chat_id_info["account_token"]
        account = Account.objects.get(account_token=account_token)
        consumer = Consumer.objects.get(account=account, type=ConsumerType.TELEGRAM)
        consumer.data["tg_chat_id"] = chat_id_info["chat_id"]
        consumer.save()
        breakpoint()
        return Response(chat_id_info, status=status.HTTP_200_OK)


class CreateConsumerApiView(APIView):
    def post(self, request):
        account = request.user.account
        account.account_token = uuid.uuid4().hex
        breakpoint()
        account.save()

        Consumer.objects.create(account=account, type=ConsumerType.TELEGRAM)
        join_url = f"https://t.me/cryptostock_2021_bot?start={account.account_token}"

        data = {"join_url": join_url}
        return Response(data, status=status.HTTP_201_CREATED)
