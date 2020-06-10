from django.urls import register_converter, path

from social_network.core.converters import UUIDConverter
from social_network.users.api.views import (
    UserProfileRetrieveAPIView,
    UserActivityRetrieveAPIView,
)

register_converter(UUIDConverter, "uuid")

urlpatterns = [
    path("profile/", UserProfileRetrieveAPIView.as_view()),
    path("<uuid:user_uuid>/activity/", UserActivityRetrieveAPIView.as_view()),
]
