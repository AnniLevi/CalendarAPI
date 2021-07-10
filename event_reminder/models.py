from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, null=True, blank=True, related_name='country_user')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

