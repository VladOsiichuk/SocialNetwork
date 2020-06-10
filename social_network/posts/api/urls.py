from django.urls import include, path, register_converter

from social_network.core.converters import UUIDConverter
from social_network.posts.api.views import PostAPIViewSet, PostVoteCreateDeleteAPIView
from rest_framework.routers import DefaultRouter

posts_router = DefaultRouter(trailing_slash=True)
posts_router.register("", PostAPIViewSet, basename="posts")

register_converter(UUIDConverter, "uuid")

urlpatterns = [
    path("<uuid:post_uuid>/votes/", PostVoteCreateDeleteAPIView.as_view()),
    path("", include(posts_router.urls)),
]
