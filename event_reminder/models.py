from django.db import models
from django.contrib.auth.models import AbstractUser
from event_reminder.managers import CustomUserManager


class CustomUser(AbstractUser):
    username = models.CharField(max_length=20, null=True, blank=True, default=None)
    email = models.EmailField(unique=True)
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, null=True, blank=True, related_name='country_user')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

