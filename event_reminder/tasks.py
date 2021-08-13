import datetime
import pytz
from celery import shared_task
from django.core.mail import send_mail
from django.db.models import Q
from CalendarAPI.settings import TIME_ZONE, DEFAULT_FROM_EMAIL
from event_reminder.models import Event, Holiday
from django.core.management import call_command


@shared_task
def remind_about_event():
    tz = pytz.timezone(TIME_ZONE)
    today = datetime.datetime.now(tz=tz)
    events = Event.objects.filter(Q(reminded=False, remind_time__lte=today)).select_related('user')
    for event in events:
        send_mail(
            subject="Event reminder",
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[event.user.email],
            message=f'Reminder.\n'
                    f'On {event.datetime_start.date()} from {event.datetime_start.time()} to {event.time_end}\n'
                    f'you have an event scheduled: {event.name}.',
        )
        event.reminded = True
        event.save()


@shared_task
def update_holidays():
    Holiday.objects.delete()
    call_command("get_holidays", )
