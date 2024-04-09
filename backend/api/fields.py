import jwt

from datetime import datetime, timedelta
from django.conf import settings
from rest_framework import serializers

from api.models import User
from api.utils import create_access_token


class AccessTokenCreate(serializers.Field):
    def to_internal_value(self, obj):
        access_token = create_access_token(obj)
        return access_token


class AccessTokenView(serializers.Field):
    def to_representation(self, value):
        return value

