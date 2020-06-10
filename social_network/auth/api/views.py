from typing import Any

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from social_network.core.api.views import ProjectCreateAPIView
from social_network.auth.api.serializers import (
    UserRegisterSerializer,
    UserLoginSerializer,
)


class UserRegisterAPIView(ProjectCreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserRegisterSerializer


class UserLoginAPIView(TokenObtainPairView):
    serializer_class = UserLoginSerializer
