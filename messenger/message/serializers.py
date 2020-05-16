from rest_framework import serializers
from message.models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'user', 'text', 'created', 'username']
        read_only_fields = ['username']

    username = serializers.SerializerMethodField()

    def get_username(self, obj):
        return obj.user.username

    def create(self, validated_data):
        message = Message(**validated_data)
        message.save()
        return message
