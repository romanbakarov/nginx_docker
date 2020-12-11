from rest_framework import mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from social_network_api.models import Post, Like
from social_network_api.serializer import PostSerializer, LikeSerializer


class PostViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class LikeView(mixins.UpdateModelMixin, GenericViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'post'

    def get_object(self):
        obj, _ = Like.objects.get_or_create(user=self.request.user,
                                            post_id=self.kwargs['post'])

        return obj
