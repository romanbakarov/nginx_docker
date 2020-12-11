from django.db.models import Case, When, Count
from django_filters import rest_framework as filters
from rest_framework import mixins, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from social_network_api.filters import LikeAnalyticsFilter
from social_network_api.models import Post, Like
from social_network_api.serializer import PostSerializer, LikeSerializer, LikeAnalyticsSerializer


class PostViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    """
    Lists and creates posts
    """
    queryset = Post.objects.all().annotate(
        likes_count=Count(Case(When(like__like=True, then=1))))
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


class LikeAnalyticsView(generics.ListAPIView):
    """
    Returns analytics about how many likes was made
    aggregated by day
    """
    queryset = Like.objects.all().annotate(
        likes_count=Count(Case(When(like=True, then=1)))).order_by('-liked_at')
    permission_classes = [IsAuthenticated]
    serializer_class = LikeAnalyticsSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = LikeAnalyticsFilter
