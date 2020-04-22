from rest_framework import serializers
from message.models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'user', 'text', 'created']

    def create(self, validated_data):
        message = Message(**validated_data)
        message.save()
        return message
