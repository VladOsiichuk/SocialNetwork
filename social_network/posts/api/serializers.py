from typing import Dict, Any

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request

from social_network.posts.models import Post, Vote

User = get_user_model()


class NestedAuthorSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    uuid = serializers.UUIDField(read_only=True, format="hex")
    last_request = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = ("uuid", "username", "last_request")


class PostListSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True, format="hex")
    count_likes = serializers.IntegerField(read_only=True)
    count_dislikes = serializers.IntegerField(read_only=True)
    is_liked = serializers.BooleanField(read_only=True, default=False)
    is_disliked = serializers.BooleanField(read_only=True, default=False)
    title = serializers.CharField(read_only=True)
    author = NestedAuthorSerializer(read_only=True)

    class Meta:
        model = Post
        fields = (
            "uuid",
            "count_likes",
            "count_dislikes",
            "title",
            "is_liked",
            "is_disliked",
            "author",
        )


class PostDetailSerializer(PostListSerializer):
    uuid = serializers.UUIDField(read_only=True, format="hex")
    body = serializers.CharField(max_length=10000, required=True, allow_null=False)
    title = serializers.CharField(max_length=128, required=True, allow_null=False)
    is_published = serializers.BooleanField(
        required=False, allow_null=False, default=False, write_only=True
    )

    class Meta:
        model = Post
        fields = (
            "uuid",
            "is_published",
            "body",
            "count_likes",
            "count_dislikes",
            "title",
            "is_liked",
            "is_disliked",
            "author",
        )

    def validate(self, attrs: Dict[str, str]) -> Dict[str, str]:
        request = self.context.get("request")
        user = request.user
        if self.instance is not None and self.instance.author_id != user.id:
            raise PermissionDenied

        return attrs

    def create(self, validated_data: Dict[str, Any]) -> Post:
        request = self.context.get("request")
        user = request.user
        validated_data["author"] = user
        return super().create(validated_data)


class PostVoteSerializer(serializers.ModelSerializer):
    vote = serializers.ChoiceField(required=True, choices=Vote.VOTE_CHOICES)
    uuid = serializers.UUIDField(read_only=True, format="hex")

    class Meta:
        model = Vote
        fields = ("vote", "uuid")

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        request: Request = self.context.get("request")
        post = get_object_or_404(
            Post.objects.filter(is_active=True, is_published=True),
            uuid=request.parser_context["kwargs"]["post_uuid"],
        )
        attrs["post"] = post
        attrs["user"] = request.user
        return attrs

    def create(self, validated_data: Dict[str, str]) -> Vote:
        post = validated_data.pop("post")
        user = validated_data.pop("user")
        vote = post.add_vote_from_user(user, validated_data["vote"])
        return vote
