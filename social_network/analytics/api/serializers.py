from rest_framework import serializers

from social_network.posts.models import Vote


class VoteListSerializer(serializers.ModelSerializer):
    count_votes = serializers.IntegerField(read_only=True)
    date = serializers.DateTimeField(format="%Y-%m-%d")

    class Meta:
        model = Vote
        fields = ("count_votes", "date")
