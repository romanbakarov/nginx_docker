from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase

from social_network_api.models import Post
from social_network_api.serializer import PostSerializer


class PostApiTest(APITestCase):
    def test_get(self):
        user = User.objects.create(username='user1', password='test1234')
        post_1 = Post.objects.create(author=user, body='test body 1')
        post_2 = Post.objects.create(author=user, body='test body 2')
        url = reverse('post-list')
        response = self.client.get(url)
        serializer_data = PostSerializer([post_1, post_2], many=True).data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer_data)
