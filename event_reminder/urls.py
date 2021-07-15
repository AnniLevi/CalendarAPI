from django.contrib import admin
from django.urls import path
from event_reminder.views import RegisterAPI, GetTokenAPI, EventCreateAPI

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegisterAPI.as_view(), name='register'),
    path('get_token/', GetTokenAPI.as_view(), name='get-token'),
    path('create_event/', EventCreateAPI.as_view(), name='create-event'),
]
