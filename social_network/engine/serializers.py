from rest_framework import serializers

from engine.models import Posts, PostLikes
from users.serializers import UserSerializer


class PostLikesSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True, default=None)

    class Meta:
        model = PostLikes
        fields = ('owner',)


class PostsSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True, default=None)
    likes = PostLikesSerializer(read_only=True, many=True, default=[])

    class Meta:
        model = Posts
        fields = ('id', 'author', 'text', 'likes', 'likes_count', 'created_at')
