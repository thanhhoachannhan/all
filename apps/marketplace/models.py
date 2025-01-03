from django.db import models
from authentication.models import User

class MarketplaceUserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(user_type='marketplace')

class MarketplaceUser(User):
    marketplace = models.BooleanField(default=True)

    objects = MarketplaceUserManager()

    class Meta:
        # proxy = True # chi them khi ko them fiels ma chi them logic
        verbose_name = "Marketplace User"
        verbose_name_plural = "Marketplace Users"