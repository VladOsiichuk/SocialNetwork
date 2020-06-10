from django.db.models import Count
from django.db.models.functions import TruncDay
from django.db.models.query import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAdminUser

from social_network.analytics.api.filters import VoteFilterSet
from social_network.analytics.api.serializers import VoteListSerializer
from social_network.core.api.views import ProjectListAPIView
from social_network.posts.models import Vote


class VoteAnalyticAPIView(ProjectListAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = VoteListSerializer
    filterset_class = VoteFilterSet
    filter_backends = (OrderingFilter, DjangoFilterBackend)

    def get_queryset(self) -> QuerySet:
        qs = (
            Vote.objects.annotate(date=TruncDay("created_at"))
            .values("date")
            .annotate(count_votes=Count("id"))
            .values("date", "count_votes")
        )
        return qs
