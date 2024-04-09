import json
import jwt

from datetime import datetime, timedelta

from django.core.cache import cache
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.conf import settings
from api.models import User
from api.serializers import (
    AllSerializer,
    LoginSerializer,
    LogoutSerializer,
    RefreshSerializer,
    RegistrationSerializer,
    UserDataSerializer,
)
from api.utils import create_refresh_token


class AllAPIView(APIView):
    serializer_class = AllSerializer

    def get(self, request):
        users = User.objects.filter(is_active=True)
        serializer = self.serializer_class(users, many=True)
        return Response(serializer.data)


class LoginAPIView(APIView):
    serializer_class = LoginSerializer

    def get(self, request):
        user = get_object_or_404(User, email=request.data.get('email'))
        serializer = self.serializer_class(user)
        return Response(serializer.data)


class LogoutAPIView(APIView):
    serializer_class = LogoutSerializer

    def post(self, request):
        user = get_object_or_404(User, refresh_token=request.data.get('refresh_token'))
        data = {
            'is_active': False,
        }
        serializer = self.serializer_class(user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success": "User logged out."})


class RefreshAPIView(APIView):
    serializer_class = RefreshSerializer

    def post(self, request):
        user = get_object_or_404(User, refresh_token=request.data.get('refresh_token'))
        data = {
            'refresh_token': create_refresh_token(user.email),
        }
        serializer = self.serializer_class(user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class RegistrationAPIView(APIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        password = request.data.get('password', '')
        email = request.data.get('email', '')
        data = {
            'password': password,
            'email': email,
        }
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = User.objects.get(email=email)
        response_data = {
            'id': user_data.id,
            'email': email,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

class UserDataAPIView(APIView):
    serializer_class = UserDataSerializer

    def get(self, request):
        email = cache.get('email').split()[0]
        user = get_object_or_404(User, email=email)
        serializer = self.serializer_class(user, many=False)
        return Response(serializer.data)

    def put(self, request):
        email = cache.get('email').split()[0]
        user = get_object_or_404(User, email=email)
        username = request.data.get('username', '')
        data = {
            'username': username,
        }
        serializer = self.serializer_class(user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
