from rest_framework import serializers
from .models import Post, Comment, Like


class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username")
    like_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = ["id", "title", "content", "author", "like_count", "created_at"]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username")

    class Meta:
        model = Comment
        fields = ["id", "content", "author", "parent", "created_at"]


class LikeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["user", "post", "comment"]

    def validate(self, data):
        if not data.get("post") and not data.get("comment"):
            raise serializers.ValidationError("Provide post or comment.")
        if data.get("post") and data.get("comment"):
            raise serializers.ValidationError("Only one allowed.")
        return data
