from rest_framework import serializers
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

    def create(self, validated_data):
        user = User(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user

    # def validated_data(self, data):
    #     if all(i in ['username', 'password'] for i in data.keys):
    #         print(data)
    #         return data
    #     raise serializers.ValidationError('Not every field defined')
