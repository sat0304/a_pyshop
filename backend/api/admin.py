from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import path

from api.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'is_active',
        'is_staff',
        'created_at',
        'updated_at',
        'refresh_token',
    )
    list_display_links = (
        'id',
        'username',
        'email',
    )
    ordering = 'id',
