import os

from rest_framework import serializers

ALLOWED_TELEGRAM_BOTS_NAMES = [os.environ["TELEGRAM_BOT_NAME"]]


class FromTelegramDataSerializer(serializers.Serializer):
    account_token = serializers.CharField(max_length=32, min_length=32)
    chat_id = serializers.IntegerField()
    source = serializers.CharField()

    def validate_source(self, value):
        if value not in ALLOWED_TELEGRAM_BOTS_NAMES:
            raise serializers.ValidationError(f"Source {value} not allowed.")


class CreateConsumerSerializer(serializers.Serializer):
    recipient = serializers.EmailField(required=False)
