from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from ecommerce.models import EcommerceUser


@admin.register(EcommerceUser)
class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {
            'fields': ('username', 'password', 'fullname', 'email', 'avatar', 'address', 'groups', 'user_type')
        }),
        ('Advanced options', {
            'classes': ('collapse'),
            'fields': ('user_permissions', 'is_active', 'is_staff', 'is_superuser', 'is_buyer', 'is_seller', 'is_shiper')
        })
    )
    list_display = ('username', 'email', 'date_joined')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('username__startswith', 'fullname__startswith')

    class Meta:
        ordering = ('date_joined')

for model in apps.get_app_config('ecommerce').get_models():
    try: admin.site.register(model)
    except AlreadyRegistered: pass
