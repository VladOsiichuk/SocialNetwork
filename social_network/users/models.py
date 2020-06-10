import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    last_request = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users"
