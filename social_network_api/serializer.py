from rest_framework import serializers

from social_network_api.models import Post, Like


class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'author', 'body')


class LikeSerializer(serializers.ModelSerializer):
    post = serializers.ReadOnlyField(source='post.id')

    class Meta:
        model = Like
        fields = ('like', 'post')
