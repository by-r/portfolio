from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from portfolio.models import Post

DEMO_USERNAME = "admin"
DEMO_PASSWORD = "admin"
DEMO_EMAIL = "admin@example.test"

DEMO_POSTS = [
    {
        "slug": "welcome-to-my-portfolio",
        "title": "Welcome to my portfolio",
        "content": (
            "# Welcome\n\n"
            "This is my portfolio and blog, built with **Django**, **React**, and "
            "a focus on keeping things simple.\n\n"
            "Here I share projects, notes, and things I learn along the way."
        ),
        "is_published": True,
    },
    {
        "slug": "building-this-site",
        "title": "Building this site",
        "content": (
            "# Building this site\n\n"
            "This site uses a read-only API, Markdown-authored posts, and a lightweight "
            "frontend. The goal is a fast, secure home for my work.\n\n"
            "The development environment is fully self-initializing with Docker."
        ),
        "is_published": True,
    },
]


class Command(BaseCommand):
    help = "Create the development admin and two published demo posts (DEBUG only)."

    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise CommandError("seed_demo is only available when DEBUG=True.")

        self.stdout.write(
            self.style.WARNING(
                "WARNING: admin:admin is for development/demo use only; "
                "never use these credentials in production."
            )
        )

        user_model = get_user_model()
        with transaction.atomic():
            user, _ = user_model.objects.get_or_create(username=DEMO_USERNAME)
            user.email = DEMO_EMAIL
            user.is_staff = True
            user.is_superuser = True
            user.set_password(DEMO_PASSWORD)
            user.save()

            for post in DEMO_POSTS:
                Post.objects.update_or_create(slug=post["slug"], defaults=post)

        self.stdout.write(
            self.style.SUCCESS(
                f"seed_demo: ensured {DEMO_USERNAME} and {len(DEMO_POSTS)} published post(s)."
            )
        )
