from django.contrib.auth import get_user_model
from django.db.models import Count, Case, When
from django.urls import reverse, resolve
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from social_network_api.models import Post, Like
from social_network_api.serializer import PostSerializer

from freezegun import freeze_time

Account = get_user_model()


class PostApiTest(APITestCase):
    def setUp(self) -> None:
        self.user1 = Account.objects.create_user(email='user1@user.com', username='username1', password='password')
        self.user2 = Account.objects.create_user(email='user2@user.com', username='username2', password='password')
        self.post1 = Post.objects.create(author=self.user1, body='test1')
        self.post2 = Post.objects.create(author=self.user1, body='test2')
        self.user1_credentials = {
            'email': 'user1@user.com',
            'password': 'password'
        }
        self.user2_credentials = {
            'email': 'user2@user.com',
            'password': 'password'
        }
        self.url = reverse('accounts:token_obtain_pair')
        response_from_user1 = self.client.post(self.url, self.user1_credentials)
        response_from_user2 = self.client.post(self.url, self.user1_credentials)
        self.user1_token = response_from_user1.data['access']
        self.user2_token = response_from_user2.data['access']

    def test_list(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user1_token)
        url = reverse('post-list')
        response = self.client.get(url)
        posts = Post.objects.all().annotate(
            likes_count=Count(Case(When(like__like=True, then=1))))
        serializer_data = PostSerializer(posts, many=True).data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer_data)

    def test_create_post_when_user_is_anon(self):
        url = reverse('post-list')
        data = {
            'body': 'test'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_post_when_user_is_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user1_token)
        url = reverse('post-list')
        data = {
            'body': 'test'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Post.objects.last().body, 'test')

    def test_detail(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user1_token)
        url = reverse('post-detail', kwargs={'pk': self.post1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['author'], 'username1')
        self.assertEqual(response.data['body'], 'test1')


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class LikeApiTest(APITestCase):

    def setUp(self) -> None:
        self.user1 = Account.objects.create_user(email='user1@user.com', username='username1', password='password')
        self.user2 = Account.objects.create_user(email='user2@user.com', username='username2', password='password')
        self.token1 = get_tokens_for_user(self.user1)['access']
        self.post = Post.objects.create(author=self.user2, body='test1')

    def test_post_like(self):
        url = reverse('like-detail', kwargs={'post': self.post.id})
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token1)
        response = self.client.patch(url, {'like': 'True'})
        expected_data = {
            'post': self.post.id,
            'like': True
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_data)

    def test_post_unlike(self):
        url = reverse('like-detail', kwargs={'post': self.post.id})
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token1)
        response = self.client.patch(url, {'like': False})
        expected_data = {
            'post': self.post.id,
            'like': False
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_data)


class LikeAnalyticsTestApi(APITestCase):
    def setUp(self) -> None:
        self.user1 = Account.objects.create_user(email='user1@user.com', username='username1', password='password')
        self.user2 = Account.objects.create_user(email='user2@user.com', username='username2', password='password')
        self.post = Post.objects.create(author=self.user2, body='test1')
        Like.objects.create(post=self.post, user=self.user1)

    @freeze_time('2020-12-12')
    def test_like_analytics(self):
        token = get_tokens_for_user(self.user2)['access']
        url = reverse('like-detail', kwargs={'post': self.post.id})
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        self.client.patch(url, {'like': 'True'})
        expected_data = [
            {
                'likes_count': 1,
                'liked_at': '2020-12-12'
            },
            {
                'likes_count': 1,
                'liked_at': '2020-12-11'
            }
        ]
        url = reverse('likes_analytics')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_data)


