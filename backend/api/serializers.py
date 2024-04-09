import jwt

from datetime import datetime, timedelta
from django.conf import settings
from rest_framework import serializers

from api.fields import AccessTokenCreate, AccessTokenView
from api.models import User
from api.utils import create_access_token


class AllSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = 'id', 'email', 'username', 'is_active', 'is_staff', 'refresh_token'


class LoginSerializer(serializers.ModelSerializer):
    access_token = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = (
            'access_token',
            'refresh_token',
        )

    def get_access_token(self, obj):
        access_token = create_access_token(obj)
        return access_token


class LogoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'is_active',
        )

class RefreshSerializer(serializers.ModelSerializer):
    access_token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'access_token',
            'refresh_token',
        )

    def get_access_token(self, obj):
        access_token = create_access_token(obj)
        return access_token


class RegistrationSerializer(serializers.ModelSerializer):
    """ Сериализация регистрации пользователя и создания нового. """
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = (
            'email',
            'password',
        )

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = 'id', 'email', 'username',
