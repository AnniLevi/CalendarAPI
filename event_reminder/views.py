from django.contrib.auth import authenticate
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.generics import GenericAPIView, CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from event_reminder.models import Event, Holiday
from event_reminder.serializers import RegisterSerializer, UserSerializer, EventSerializer, HolidaySerializer
from CalendarAPI.settings import DEFAULT_FROM_EMAIL
from collections import defaultdict


class RegisterAPI(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.create(user=user).__str__()
        recipient_email = request.data.get('email')
        send_mail(
            subject="Registration message",
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            message=f'You have successfully registered.\nYour token: {token}',
        )
        return Response(
            {
                "user": UserSerializer(user).data,
                "token": token,
             },
            status=status.HTTP_201_CREATED
        )


class GetTokenAPI(APIView):
    def post(self, request):
        user = authenticate(
            email=request.data['email'],
            password=request.data['password']
        )
        if user is not None:
            token = Token.objects.get_or_create(user=user)[0].__str__()
            send_mail(
                subject="Your token",
                from_email=DEFAULT_FROM_EMAIL,
                recipient_list=[request.data.get('email')],
                message=f'Your token: {token}',
            )
            return Response({"token": token}, status=status.HTTP_200_OK)
        return Response('User with such data does not exist', status=status.HTTP_400_BAD_REQUEST)


class EventCreateAPI(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DayEventsAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer

    def get(self, request, *args, **kwargs):
        date = request.data.get('date')
        queryset = Event.objects.filter(user_id=self.request.user.id, datetime_start__date=date)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MonthEventsAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer

    def get(self, request, *args, **kwargs):
        month = request.data.get('month')
        queryset = Event.objects.filter(user_id=self.request.user.id, datetime_start__month=month)
        result = defaultdict(list)
        for event in queryset:
            result[str(event.datetime_start.date())].append(self.serializer_class(event).data)
        return Response(result, status=status.HTTP_200_OK)


class MonthHolidaysAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HolidaySerializer

    def get(self, request, *args, **kwargs):
        month = request.data.get('month')
        queryset = Holiday.objects.filter(country=self.request.user.country, date_start__month=month)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

