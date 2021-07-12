from django.contrib import admin
from django.urls import path
from event_reminder.views import RegisterAPI, GetToken

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegisterAPI.as_view(), name='register'),
    path('get_token/', GetToken.as_view(), name='get-token'),
]
