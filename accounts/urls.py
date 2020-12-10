from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import AccountCreate, AccountActivity

app_name = 'accounts'

urlpatterns = [
    path('signup/', AccountCreate.as_view(), name='create_account'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('activity/<int:pk>', AccountActivity.as_view(), name='account_activity')
]
