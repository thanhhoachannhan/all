from django.db import models
from authentication.models import User

class TestUserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(user_type='test')

class TestUser(User):
    test = models.BooleanField(default=True)

    objects = TestUserManager()

    class Meta:
        # proxy = True # chi them khi ko them fiels ma chi them logic
        verbose_name = "Test User"
        verbose_name_plural = "Test Users"