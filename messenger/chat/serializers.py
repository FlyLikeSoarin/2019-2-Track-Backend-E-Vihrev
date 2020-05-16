from rest_framework import serializers
from chat.models import Chat, Member
from message.models import Message
from message.serializers import MessageSerializer


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'chat_label', 'chatLabel', 'lastMessage']
        read_only_fields = ['chatLabel', 'lastMessage']

    chatLabel = serializers.CharField(source='chat_label')
    lastMessage = serializers.SerializerMethodField()

    def get_lastMessage(self, obj):
        lastMessageQS = Message.objects.all().filter(chat=obj).order_by('-created')
        if lastMessageQS.exists():
            return MessageSerializer(lastMessageQS[0]).data
        else:
            return 'None'

    def validated_data(self, data):
        if all(i in ['chat_label', 'icon'] for i in data):
            return data
        raise serializers.ValidationError('Not every field defined')


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['user', 'last_unseen']
        depth = 1
