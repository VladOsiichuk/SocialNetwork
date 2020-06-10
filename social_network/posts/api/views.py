from typing import Any

from django.contrib.contenttypes.models import ContentType
from django.db.models import QuerySet, Count, Q, Exists, OuterRef
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.viewsets import ModelViewSet

from social_network.core.api.views import ProjectCreateAPIView
from social_network.posts.api.serializers import (
    PostListSerializer,
    PostDetailSerializer,
    PostVoteSerializer,
)
from social_network.posts.models import Post, Vote


class PostAPIViewSet(ModelViewSet):
    lookup_field = "uuid"
    lookup_url_kwarg = "post_uuid"
    http_method_names = ["get", "head", "post", "patch", "put", "options"]
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        __ = {"list": PostListSerializer}
        return __.get(self.action, PostDetailSerializer)

    def get_queryset(self) -> QuerySet:

        queryset = Post.objects.filter(is_active=True, is_published=True).annotate(
            count_likes=Count(
                "votes", filter=Q(votes__vote=Vote.VOTE_CHOICES.LIKE), distinct=True
            ),
            count_dislikes=Count(
                "votes", filter=Q(votes__vote=Vote.VOTE_CHOICES.DISLIKE), distinct=True
            ),
        )

        user = self.request.user
        if user.is_authenticated:

            queryset = queryset.annotate(
                is_liked=Exists(
                    Vote.objects.filter(
                        user_id=user.id,
                        post_id=OuterRef("id"),
                        vote=Vote.VOTE_CHOICES.LIKE,
                    )
                ),
                is_disliked=Exists(
                    Vote.objects.filter(
                        user_id=user.id,
                        post_id=OuterRef("id"),
                        vote=Vote.VOTE_CHOICES.DISLIKE,
                    )
                ),
            )

        return queryset


class PostVoteCreateDeleteAPIView(ProjectCreateAPIView):
    http_method_names = ["options", "post", "delete"]
    permission_classes = (IsAuthenticated,)
    serializer_class = PostVoteSerializer

    def delete(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        post = get_object_or_404(
            Post.objects.filter(is_active=True, is_published=True),
            uuid=self.kwargs["post_uuid"],
        )
        post.remove_vote_from_user(request.user)
        return Response(status=HTTP_204_NO_CONTENT)
