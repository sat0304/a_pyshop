
from django.contrib.auth.models import (
    AbstractBaseUser,
    AbstractUser,
    BaseUserManager,
    PermissionsMixin
)
from django.db import models
from api.utils import create_refresh_token


class UserManager(BaseUserManager):

    def create_user(self, email,  password,):
        """ Создает и возвращает пользователя с имэйлом, паролем и именем. """
        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(
            email=self.normalize_email(email),
            password=password,
            refresh_token=create_refresh_token(email),

    )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self,  email, password,):
        """ Создает и возввращет пользователя с привилегиями суперадмина. """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, password,)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractUser):
    username = models.CharField(max_length=255, blank=True,)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    refresh_token = models.CharField(max_length=1024, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username
