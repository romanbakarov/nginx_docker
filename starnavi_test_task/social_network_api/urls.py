from django.urls import path
from rest_framework.routers import DefaultRouter

from social_network_api.views import PostViewSet, LikeView, LikeAnalyticsView

router = DefaultRouter()
router.register(r'post', PostViewSet)
router.register(r'post_like', LikeView)

urlpatterns = [
    path('analytics/', LikeAnalyticsView.as_view(), name='likes_analytics')
]

urlpatterns += router.urls
