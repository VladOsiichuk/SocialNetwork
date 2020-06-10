from typing import Dict, Any

from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(format="hex", read_only=True)
    password = serializers.CharField(
        required=True, max_length=256, write_only=True, min_length=8
    )
    password_confirm = serializers.CharField(
        required=True, max_length=256, write_only=True, min_length=8
    )
    username = serializers.CharField(
        required=True,
        max_length=256,
        validators=(UniqueValidator(queryset=User.objects.all()),),
    )

    class Meta:
        model = User
        fields = ("uuid", "password", "password_confirm", "username")

    def validate(self, attrs: Dict[str, str]) -> Dict[str, str]:
        if attrs["password"] != attrs["password_confirm"]:
            error_msg = _("Passwords must match")
            raise ValidationError(
                {"password": error_msg, "password_confirm": error_msg}
            )

        attrs.pop("password_confirm")
        return attrs

    def create(self, validated_data: Dict[str, str]) -> User:
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user


class UserLoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        data = super().validate(attrs)
        self.user.last_login = timezone.now()
        self.user.save()
        return data
