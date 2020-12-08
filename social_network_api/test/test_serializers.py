from datetime import datetime, timezone

from django.test import TestCase
from django.contrib.auth import get_user_model

from social_network_api.models import Post
from social_network_api.serializer import PostSerializer

account = get_user_model()


class PostSerializerTestCase(TestCase):
    def test_ok(self):
        user = account.objects.create(email='user@mail.com', username='user1', password='test1234')
        post_1 = Post.objects.create(author=user, body='test body 1')
        post_2 = Post.objects.create(author=user, body='test body 2')
        data = PostSerializer([post_1, post_2], many=True).data
        expected_data = [
            {
                'id': post_1.id,
                'author': user.id,
                'body': 'test body 1',
                'created_at': datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
            },
            {
                'id': post_2.id,
                'author': user.id,
                'body': 'test body 2',
                'created_at': datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
            }
        ]
        self.assertEqual(data, expected_data)
