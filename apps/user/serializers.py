
from rest_framework import serializers
from django.contrib.auth import authenticate


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])

        # User doesn't exists in the system.
        if user is None:
            raise serializers.ValidationError('No active account found with the given credentials')
        data['user'] = user
        return data
