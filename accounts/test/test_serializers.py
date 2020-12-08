from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.serializers import AccountSerializer

User = get_user_model()


class AccountSerializerTestCase(TestCase):
    def test_ok(self):
        user1 = User.objects.create(email='user1@user.com', username='username1', password='password')
        user2 = User.objects.create(email='user2@user.com', username='username2', password='password')
        data = AccountSerializer([user1, user2], many=True).data
        expected_data = [
            {
                'email': 'user1@user.com',
                'username': 'username1'
            },
            {
                'email': 'user2@user.com',
                'username': 'username2'
            }
        ]
        self.assertEqual(data, expected_data)
