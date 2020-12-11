from rest_framework import serializers

from social_network_api.models import Post, Like


class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(read_only=True)
    likes_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'author', 'body', 'likes_count')


class LikeSerializer(serializers.ModelSerializer):
    post = serializers.ReadOnlyField(source='post.id')

    class Meta:
        model = Like
        fields = ('like', 'post')


class LikeAnalyticsSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(read_only=True)
    liked_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%d")

    class Meta:
        model = Like
        fields = ('likes_count', 'liked_at')
