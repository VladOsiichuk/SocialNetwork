from django.urls import path
from social_network.analytics.api.views import VoteAnalyticAPIView

urlpatterns = [path("votes/", VoteAnalyticAPIView.as_view())]
