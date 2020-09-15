from rest_framework import serializers

from posts.models import Like, Post
from users.serializers import DefaultUserSerializer


class LikeSerializer(serializers.ModelSerializer):
    created_by = DefaultUserSerializer()

    class Meta:
        model = Like
        fields = ("created_at", "created_by")
        read_only_fields = ("created_at",)


class PostSerializer(serializers.ModelSerializer):
    likes = LikeSerializer(many=True, required=False)
    created_by = DefaultUserSerializer(required=False)

    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = (
            "created_at",
            "created_by",
            "likes",
        )
