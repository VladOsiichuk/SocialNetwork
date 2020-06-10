from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices

from social_network.core.models import AbstractBaseModel

User = get_user_model()


class Post(AbstractBaseModel):
    title = models.CharField(max_length=128, null=False)
    body = models.CharField(max_length=10000)
    author = models.ForeignKey(
        User, related_name="posts", on_delete=models.PROTECT, null=True
    )
    is_active = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        db_table = "posts"

    def remove_vote_from_user(self, user: User) -> None:
        self.votes.filter(user_id=user.id).delete()

    def add_vote_from_user(self, user: User, vote_type: str) -> "Vote":
        # May be a case that user liked a post and currently wants to dislike it
        # so change like to dislike
        vote, __ = self.votes.update_or_create(
            user_id=user.id, defaults={"vote": vote_type}
        )
        return vote


class Vote(AbstractBaseModel):
    VOTE_CHOICES = Choices(("LIKE", _("Like")), ("DISLIKE", _("Dislike")))

    user = models.ForeignKey(User, related_name="votes", on_delete=models.CASCADE)
    vote = models.CharField(max_length=32, choices=VOTE_CHOICES)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="votes")

    class Meta:
        db_table = "posts_votes"
        unique_together = ("user_id", "post_id")
