from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from media_test.views import image_upload

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('social_network_api.urls')),
    path('api-auth/', include('accounts.urls', namespace='accounts')),
    path("upload/", image_upload, name="upload"),
]

if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
