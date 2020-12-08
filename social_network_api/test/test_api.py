from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase

from social_network_api.models import Post
from social_network_api.serializer import PostSerializer


Account = get_user_model()


class PostApiTest(APITestCase):
    def test_get(self):
        user = Account.objects.create(username='user1', password='test1234')
        post_1 = Post.objects.create(author=user, body='test body 1')
        post_2 = Post.objects.create(author=user, body='test body 2')
        url = reverse('post-list')
        response = self.client.get(url)
        serializer_data = PostSerializer([post_1, post_2], many=True).data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer_data)
