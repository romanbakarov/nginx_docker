from django.contrib import admin
from django.urls import path
from rest_framework.routers import SimpleRouter

from social_network_api.views import PostViewSet

router = SimpleRouter()

router.register(r'post', PostViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += router.urls
