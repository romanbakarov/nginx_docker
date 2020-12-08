from django.urls import path
from .views import AccountCreate

app_name = 'accounts'

urlpatterns = [
    path('create/', AccountCreate.as_view(), name='create_account'),
]
