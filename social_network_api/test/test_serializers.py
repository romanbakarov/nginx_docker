from django.db.models import Count, Case, When
from django.test import TestCase
from django.contrib.auth import get_user_model

from social_network_api.models import Post, Like
from social_network_api.serializer import PostSerializer, LikeSerializer

account = get_user_model()


class PostSerializerTestCase(TestCase):
    def test_ok(self):
        user1 = account.objects.create(email='user1@mail.com', username='user1', password='test1234')
        user2 = account.objects.create(email='user2@mail.com', username='user2', password='test1234')

        post_1 = Post.objects.create(author=user1, body='test body 1')
        post_2 = Post.objects.create(author=user1, body='test body 2')
        Like.objects.create(post=post_1, user=user1, like=True)
        Like.objects.create(post=post_1, user=user2, like=True)
        posts = Post.objects.all().annotate(
            likes_count=Count(Case(When(like__like=True, then=1)))).order_by('id')
        data = PostSerializer(posts, many=True).data
        expected_data = [
            {
                'id': post_1.id,
                'author': user1.username,
                'body': 'test body 1',
                'likes_count': 2
            },
            {
                'id': post_2.id,
                'author': user1.username,
                'body': 'test body 2',
                'likes_count': 0
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
