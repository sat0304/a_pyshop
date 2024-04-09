from django.urls import include, path
from api.views import (
    AllAPIView,
    LoginAPIView,
    LogoutAPIView,
    RefreshAPIView,
    RegistrationAPIView,
    UserDataAPIView,
)

app_name = 'api'

urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name='register'),
    path('all/', AllAPIView.as_view(), name='all'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('refresh/', RefreshAPIView.as_view(), name='refresh'),
    path('me/', UserDataAPIView.as_view(), name='me'),
]