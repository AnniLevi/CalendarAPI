import datetime
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


class Event(models.Model):

    REMINDER_UNITS = (
        (60, 'minutes'),
        (3600, 'hours'),
        (86400, 'days'),
        (604800, 'weeks')
    )

    name = models.TextField()
    datetime_start = models.DateTimeField()
    time_end = models.TimeField(null=True, blank=True, default='23:59:59')
    remind_unit = models.IntegerField(choices=REMINDER_UNITS, null=True, blank=True)
    number_of_remind_units = models.SmallIntegerField(default=1)
    remind_time = models.DateTimeField(null=True, blank=True)
    reminded = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_event')

    def save(self, **kwargs):
        if self.remind_unit:
            delta = datetime.timedelta(seconds=self.remind_unit * self.number_of_remind_units)
            self.remind_time = self.datetime_start - delta
        super().save(**kwargs)

    def __str__(self):
        return self.name


class Holiday(models.Model):
    name = models.TextField()
    date_start = models.DateField()
    date_end = models.DateField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
