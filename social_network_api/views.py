from rest_framework.viewsets import ModelViewSet

from social_network_api.models import Post
from social_network_api.serializer import PostSerializer


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
