from django.urls import path
from event_reminder import views

urlpatterns = [
    path('register/', views.RegisterAPI.as_view(), name='register'),
    path('get_token/', views.GetTokenAPI.as_view(), name='get-token'),
    path('create_event/', views.EventCreateAPI.as_view()),
    path('events_for_day/', views.DayEventsAPI.as_view()),
    path('events_for_month/', views.MonthEventsAPI.as_view()),
    path('holidays_for_month/', views.MonthHolidaysAPI.as_view()),
]
