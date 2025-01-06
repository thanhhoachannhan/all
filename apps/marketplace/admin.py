from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django import forms

from marketplace.models import MarketplaceUser


class AdminSiteUserCreationForm(UserCreationForm):
    user_type = forms.ChoiceField(
        choices = settings.USER_TYPE_CHOICES,
        initial = 'marketplace',
    )

    class Meta:
        model = get_user_model()
        fields = '__all__'

@admin.register(MarketplaceUser)
class UserAdmin(UserAdmin):
    add_form = AdminSiteUserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'user_type', 'is_buyer', 'is_seller'),
        }),
    )
    fieldsets = (
        (None, {
            'fields': ('username', 'password', 'fullname', 'email', 'avatar', 'address', 'groups', 'user_type'),
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('user_permissions', 'is_active', 'is_staff', 'is_superuser', 'is_buyer', 'is_seller'),
        }),
    )
    list_display = ('username', 'email', 'date_joined')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('username__startswith', 'fullname__startswith')

    class Meta:
        ordering = ('date_joined',)


for model in apps.get_app_config('marketplace').get_models():
    try: admin.site.register(model)
    except AlreadyRegistered: pass
