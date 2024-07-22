from rest_framework import serializers

from ..models import Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.email')

    class Meta:
        model = Post
        fields = ('id', 'name', 'content', 'author', 'is_closed')

