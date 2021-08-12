from django.urls import path
from event_reminder.views import RegisterAPI, GetTokenAPI, EventCreateAPI, DayEventsAPI, MonthEventsAPI

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('get_token/', GetTokenAPI.as_view(), name='get-token'),
    path('create_event/', EventCreateAPI.as_view()),
    path('events_for_day/', DayEventsAPI.as_view()),

]
