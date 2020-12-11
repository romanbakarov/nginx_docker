from django.test import TestCase
from django.contrib.auth import get_user_model

from social_network_api.models import Post, Like
from social_network_api.serializer import PostSerializer, LikeSerializer

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
                'author': user.username,
                'body': 'test body 1',
            },
            {
                'id': post_2.id,
                'author': user.username,
                'body': 'test body 2',
            }
        ]
        self.assertEqual(data, expected_data)


class LikeSerializerTestCase(TestCase):
    def test_ok(self):
        user = account.objects.create(email='user@mail.com', username='user1', password='test1234')
        post = Post.objects.create(author=user, body='test body 1')
        like = Like.objects.create(post=post, user=user)
        data = LikeSerializer(like).data
        expected_data = {
            'post': post.id,
            'like': True
        }
        self.assertEqual(data, expected_data)
