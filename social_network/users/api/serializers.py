from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserModelSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True, format="hex")
    username = serializers.CharField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ("uuid", "username", "first_name", "last_name")
