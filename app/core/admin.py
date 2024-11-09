"""
Django admin customizaiton
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core import models


class UserAdmin(BaseUserAdmin):
    """
    Sets how the user model is listed on Django's admin interface.'
    """
    ordering = ['id']
    list_display = ['id', 'name', 'email', 'is_active', 'is_staff', 'is_superuser']
    serch_fields = ['id', 'name', 'email']


admin.site.register(models.User, UserAdmin)
