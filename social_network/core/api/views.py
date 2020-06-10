from typing import Any

from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response


class ProjectCreateAPIView(mixins.CreateModelMixin, GenericAPIView):
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return self.create(request, *args, **kwargs)


class ProjectDestroyAPIView(mixins.DestroyModelMixin):
    def delete(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return self.destroy(request, *args, **kwargs)


class ProjectListAPIView(mixins.ListModelMixin, GenericAPIView):
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return self.list(request, *args, **kwargs)
