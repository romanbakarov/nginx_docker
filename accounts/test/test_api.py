from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase, APIClient, APIRequestFactory, force_authenticate

from accounts.models import Account


class SignUpTestCase(APITestCase):
    def setUp(self) -> None:
        self.url = reverse('accounts:create_account')

    def test_post(self):
        data = {
            'email': 'user1@user.com',
            'username': 'username',
            'password': 'password'
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Account.objects.last().username, 'username')
        self.assertEqual(Account.objects.last().email, 'user1@user.com')

    def test_user_with_this_email_already_exists(self):
        user1 = Account.objects.create(email='user1@user.com', username='username1', password='password')
        data = {
            'email': 'user1@user.com',
            'username': 'username',
            'password': 'password'
        }
        with self.assertRaises(IntegrityError):
            self.client.post(self.url, data=data)

    def test_email_is_not_valid(self):
        data = {
            'email': 'user1',
            'username': 'username',
            'password': 'password'
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 400)

    def test_empty_data(self):
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, 400)


class ActivityTestCase(APITestCase):
    def setUp(self) -> None:
        User = get_user_model()
        self.user = User.objects.create_user(email='user1@user.com', username='username1', password='password')
        self.data = {
            'email': 'user1@user.com',
            'password': 'password'
        }
        self.url = reverse('accounts:token_obtain_pair')
        response = self.client.post(self.url, self.data)
        self.login_time = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        self.token = response.data['access']
        url = reverse('post-list')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        self.client.get(url, data={'format': 'json'})
        self.request_time = timezone.now().strftime("%Y-%m-%d %H:%M:%S")

    def test_activity_api_returns_valid_data(self):
        url = reverse('accounts:account_activity', kwargs={'pk': self.user.pk})
        response = self.client.get(url, data={'format': 'json'})
        expected_data = {
            'email': 'user1@user.com',
            'last_login': self.login_time,
            'last_request': self.request_time
        }
        print(response.data)
        self.assertEqual(response.data, expected_data)
