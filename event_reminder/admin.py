from django.contrib import admin

from event_reminder.models import CustomUser, Country

admin.site.register(CustomUser)
admin.site.register(Country)
