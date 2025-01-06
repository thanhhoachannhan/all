from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from authentication.models import User, UserGroup
from marketplace.models import MarketplaceUser


@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {
            'fields': ('username', 'password', 'fullname', 'email', 'avatar', 'address', 'groups', 'user_type')
        }),
        ('Advanced options', {
            'classes': ('collapse'),
            'fields': ('user_permissions', 'is_active', 'is_staff', 'is_superuser')
        })
    )
    list_display = ('username', 'email', 'date_joined')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('username__startswith', 'fullname__startswith')

    class Meta:
        ordering = ('date_joined')

    def save_model(self, request, obj, form, change):
        if change and obj.user_type == 'marketplace' and not hasattr(obj, 'marketplaceuser'):
            MarketplaceUser.objects.create(
                user_ptr=obj,
                is_buyer=True,
                is_seller=False
            )
        else:
            super().save_model(request, obj, form, change)


admin.site.unregister(Group)
@admin.register(UserGroup)
class CustomGroupAdmin(GroupAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'permissions')}),
    )
