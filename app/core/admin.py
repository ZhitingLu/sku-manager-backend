"""
Django admin customizaiton
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Used for translation of strings
from django.utils.translation import gettext_lazy as _

from core import models


class UserAdmin(BaseUserAdmin):
    """
    Sets how the custom user model is listed on Django's admin interface.
    This file customizes how the custom User model is displayed
    and managed in Django's admin interface.
    It overrides the default `UserAdmin` to provide a more
    customized display and form for the User model.
    """
    ordering = ['id']
    list_display = ['id', 'name', 'email', 'is_active', 'is_staff',
                    'is_superuser']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('Permissions'),
            {
                'fields': ('is_active', 'is_staff', 'is_superuser'),
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login']


admin.site.register(models.User, UserAdmin)
