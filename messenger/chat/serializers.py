from rest_framework import serializers
from chat.models import Chat, Member


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'chat_label']

    # def create(self, validated_data):
    #     return Comment(, **validated_data)

    def validated_data(self, data):
        if all(i in ['chat_label', 'icon'] for i in data):
            return data
        raise serializers.ValidationError('Not every field defined')


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['user', 'last_unseen']
        depth = 1
