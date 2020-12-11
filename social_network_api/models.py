from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_author')
    body = models.TextField()
    liker = models.ManyToManyField(User, through='Like', related_name='post_liker')


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    like = models.BooleanField(default=True)
    liked_at = models.DateTimeField(auto_now_add=True)
