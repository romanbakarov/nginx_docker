from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

Account = get_user_model()


class Post(models.Model):
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
