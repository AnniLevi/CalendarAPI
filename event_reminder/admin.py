from django.contrib import admin
from event_reminder.models import CustomUser, Country, Event, Holiday


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'datetime_start', 'time_end', 'reminded', 'user')
    readonly_fields = ('reminded', 'remind_time')


@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_start', 'date_end', 'country',)


admin.site.register(CustomUser)
admin.site.register(Country)

