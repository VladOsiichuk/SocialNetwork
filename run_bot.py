import json
import random
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
import django
import os

from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.prod")
django.setup()

from social_network.posts.models import Post, Vote
from django.utils import timezone


User = get_user_model()
fake = Faker()


class Bot(object):
    users_pool = []
    posts_pool = []

    def __init__(
        self, number_of_users: int, max_posts_per_user: int, max_likes_per_user: int
    ):
        self.number_of_users = number_of_users
        self.max_posts_per_user = max_posts_per_user
        self.max_likes_per_user = max_likes_per_user

    @classmethod
    def from_config_file(cls, filename: str) -> "Bot":
        with open(filename, "r") as f:
            config = json.loads(f.read())

        # provide some default values if they are missing in config
        number_of_users = config.get("number_of_users", 10)
        max_posts_per_user = config.get("max_posts_per_user", 5)
        max_likes_per_user = config.get("max_likes_per_user", 3)
        return cls(number_of_users, max_posts_per_user, max_likes_per_user)

    def _create_users(self):
        for __ in range(self.number_of_users):
            user = User(username=fake.user_name())
            user.set_password(fake.password())
            user.save()
            self.users_pool.append(user)

    def _create_posts(self):
        for user in self.users_pool:
            posts_count = random.randint(1, self.max_posts_per_user)
            for __ in range(posts_count):
                post = Post(
                    author=user,
                    title=fake.catch_phrase(),
                    body=fake.text(random.randint(1000, 3000)),
                )
                post.created_at = fake.date_this_month()
                post.is_active = True
                post.is_published = True
                post.save()
                self.posts_pool.append(post)

    def _like_posts(self):
        for user in self.users_pool:
            posts = random.sample(self.posts_pool, self.max_posts_per_user)
            for post in posts:
                Vote(user=user, post=post, vote=Vote.VOTE_CHOICES.LIKE).save()

    def _update_users_activity(self):
        for user in self.users_pool:
            user.last_login = timezone.now() - timedelta(hours=1)
            user.last_request = timezone.now()
            user.save()

    def run(self):
        self._create_users()
        self._create_posts()
        self._like_posts()
        self._update_users_activity()


if __name__ == "__main__":
    bot = Bot.from_config_file("bot_config.json")
    bot.run()
