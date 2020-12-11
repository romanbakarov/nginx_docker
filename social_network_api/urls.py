from rest_framework.routers import DefaultRouter

from social_network_api.views import PostViewSet, LikeView

router = DefaultRouter()
router.register(r'post', PostViewSet)
router.register(r'post_like', LikeView)
urlpatterns = router.urls
