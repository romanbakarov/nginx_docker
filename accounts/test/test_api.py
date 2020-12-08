from django.db import IntegrityError
from django.urls import reverse
from rest_framework.test import APITestCase

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
