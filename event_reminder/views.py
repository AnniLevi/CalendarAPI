from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.authentication import BasicAuthentication, TokenAuthentication, SessionAuthentication
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from event_reminder.models import CustomUser
from event_reminder.serializers import RegisterSerializer, UserSerializer, EventSerializer
from CalendarAPI.settings import DEFAULT_FROM_EMAIL


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
    # authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication, ]
    serializer_class = EventSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        print(serializer.data)

