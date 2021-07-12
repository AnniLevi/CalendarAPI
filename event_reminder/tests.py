from json import dumps
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from event_reminder.models import Country, CustomUser
from django.contrib.auth import get_user_model


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

        # BAD CASE
        data['email'] = 'bad_email'
        response = self.client.post(url, data=dumps(data), content_type="application/json")
        # check status 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg=response.data)
        # check user obj isn't created
        self.assertEqual(CustomUser.objects.filter(email=data['email']).exists(), False)

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
        # BAD CASE
        data['password'] = 'bad_password'
        response = self.client.post(url, data=dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg=response.data)
