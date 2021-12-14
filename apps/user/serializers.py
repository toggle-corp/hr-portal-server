from hr_portal.serializers import (
    WriteOnlyOnCreateSerializerMixin,
)
from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import User


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user_obj = User.objects.filter(username=data['username'])
        if not user_obj:
            raise serializers.ValidationError({
                "username": 'Invalid username'
            })
        else:
            user = authenticate(username=data['username'], password=data['password'])

            if user is None:
                raise serializers.ValidationError({
                    "password": 'Password doesnot match'
                })
            data['user'] = user
            return data


class UserSerializer(WriteOnlyOnCreateSerializerMixin, serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name',
                  'email',)
        write_only_on_create_fields = ('email', 'username')

    def create(self, validated_data):
        raise Exception("Create method is not used for now")

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        if 'password' in validated_data:
            user.set_password(validated_data['password'])
            user.save()
        return user
