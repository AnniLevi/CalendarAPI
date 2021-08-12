import datetime
from json import dumps
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from event_reminder.models import Country, CustomUser, Event, Holiday
from django.contrib.auth import get_user_model
from django.core import mail


class AccountTests(APITestCase):    # APITestCase use APIClient instead of Django's default Client

    def test_register(self):
        """
        Ensure we can create a new CustomUser object and Token object
        """
        url = reverse('register')
        country = Country.objects.create(name='Belarus')
        # GOOD CASE
        data = {
            'email': 'test@test.test',
            'password': 'password',
            'country': country.id,
        }
        response = self.client.post(url, data=dumps(data), content_type="application/json")
        # check status msg 201
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.data)
        self.assertEqual(response.data['user']['email'], 'test@test.test')
        self.assertEqual(response.data['user']['country'], country.id)
        # check creating user obj
        user = CustomUser.objects.get(id=response.data['user']['id'])
        self.assertEqual(response.data['user']['email'], user.email)
        self.assertEqual(response.data['user']['country'], user.country.id)
        # check creating token obj
        self.assertEqual(
            Token.objects.get(user=user).__str__(),
            response.json()['token']
        )
        # check sending of 1 message to the mail
        self.assertEqual(len(mail.outbox), 1)

        # BAD CASE
        data['email'] = 'bad_email'
        response = self.client.post(url, data=dumps(data), content_type="application/json")
        # check status 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg=response.data)
        # check user obj isn't created
        self.assertFalse(CustomUser.objects.filter(email=data['email']).exists())

    def test_get_token(self):
        """
        Ensure we can get or create token
        """
        url = reverse('get-token')
        User_model = get_user_model()   # CustomUser model
        user = User_model.objects.create_user(
            email='test@test.test',
            password='password',
            country=None
        )
        token = Token.objects.create(user=user)
        # GOOD CASE
        data = {
            'email': 'test@test.test',
            'password': 'password'
        }
        response = self.client.post(url, data=dumps(data), content_type="application/json")
        # check get token
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        self.assertEqual(response.json()['token'], token.__str__())
        # check create token
        token.delete()
        response = self.client.post(url, data=dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        self.assertEqual(
            Token.objects.get(user=user).__str__(),
            response.json()['token']
        )
        # check sending of second message to the mail
        self.assertEqual(len(mail.outbox), 2)

        # BAD CASE
        data['password'] = 'bad_password'
        response = self.client.post(url, data=dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg=response.data)


class EventsTests(APITestCase):

    def setUp(self):
        User_model = get_user_model()
        self.user = User_model.objects.create_user(
            email='test@test.test',
            password='password',
            country=None
        )
        self.client.force_authenticate(self.user)

    def test_create_event(self):
        """
        Ensure we can create a new Event object
        """
        url = reverse('create-event')
        data = {
            "name": "test_event",
            "datetime_start": "2021-08-15T15:30:00+00:00",
            "time_end": "16:00:00",
            "remind_unit": 60,
            "number_of_remind_units": 5
        }
        # GOOD CASE
        response = self.client.post(url, data=dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.data)
        # check creating event obj
        event = Event.objects.get(**data)
        self.assertEqual(response.data['id'], event.id)
        # BAD CASE
        data.pop('name')
        response = self.client.post(url, data=dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg=response.data)

    def test_events_for_day(self):
        """
        Ensure we can get events for day
        """
        url = reverse('events-day')
        day = datetime.datetime.now()
        event = Event(
            name='test_event',
            datetime_start=day,
            user_id=self.user.id
        )
        event.save()
        # GOOD CASE
        response = self.client.get(url, {'date': str(day.date())})
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        self.assertEqual(response.data[0]['id'], event.id)
        self.assertEqual(response.data[0]['name'], event.name)

    def test_events_for_month(self):
        """
        Ensure we can get events for month
        """
        url = reverse('events-month')
        day = datetime.datetime.now()
        event = Event(
            name='test_event',
            datetime_start=day,
            user_id=self.user.id
        )
        event.save()
        # GOOD CASE
        response = self.client.get(url, {'month': day.month})
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        self.assertEqual(response.data[str(day.date())][0]['id'], event.id)
        self.assertEqual(response.data[str(day.date())][0]['name'], event.name)


class HolidaysTest(APITestCase):

    def test_holidays_for_month(self):
        """
        Ensure we can get holidays for month in user's country
        """
        day = datetime.datetime.now()
        country = Country.objects.create(
            name='TestCountry'
        )
        User_model = get_user_model()
        user = User_model.objects.create_user(
            email='test@test.test',
            password='password',
            country_id=country.id
        )
        self.client.force_authenticate(user)
        holiday = Holiday.objects.create(
            name='TestHoliday',
            date_start=day.date(),
            date_end=day.date(),
            country_id=country.id
        )


        url = reverse('holidays-month')
        # GOOD CASE
        response = self.client.get(url, {'month': day.month})
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        self.assertEqual(response.data[0]['id'], holiday.id)
        self.assertEqual(response.data[0]['name'], holiday.name)
