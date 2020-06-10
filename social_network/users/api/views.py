from typing import Any

from django.contrib.auth import get_user_model
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from social_network.users.api.serializers import UserModelSerializer

User = get_user_model()


class UserProfileRetrieveAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request: Request) -> Response:
        user = request.user
        data = UserModelSerializer(user, read_only=True).data
        return Response(data)


class UserActivityRetrieveAPIView(APIView):
    permission_classes = ()

    @staticmethod
    def get(*args: Any, **kwargs: Any) -> Response:
        user = get_object_or_404(User.objects.all(), uuid=kwargs["user_uuid"])
        return Response(
            {"last_request": user.last_request, "last_login": user.last_login}
        )
