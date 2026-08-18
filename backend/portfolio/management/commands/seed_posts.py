from django.core.management.base import BaseCommand

from portfolio.models import Post

SAMPLE_POSTS = [
    {
        "title": "Hello, world",
        "content": (
            "# Hello, world\n\n"
            "This is my first post. This site is built with **Django + django-ninja** "
            "on the backend and a **Vite + React + Tailwind + Kumo UI** frontend.\n\n"
            "## What you'll find here\n\n"
            "- Notes on projects I'm working on\n"
            "- Short write-ups about tools and code\n"
            "- The occasional link dump\n\n"
            "> Keep it simple, keep it secure.\n"
        ),
        "is_published": True,
    },
    {
        "title": "A minimal portfolio, by design",
        "content": (
            "# A minimal portfolio, by design\n\n"
            "The goal here was a *simple* site: no heavy frameworks fighting each other, "
            "no analytics sprawl, just content.\n\n"
            "```python\n"
            "def portfolio():\n"
            '    return {"fast": True, "secure": True, "minimal": True}\n'
            "```\n\n"
            "Posts are written in Markdown from the Django admin and served read-only "
            "through the API. [Check out Kumo UI](https://kumo-ui.com) — it powers the "
            "components you see on this page.\n"
        ),
        "is_published": True,
    },
]


class Command(BaseCommand):
    help = "Create 1-2 sample published posts for local development (idempotent)."

    def handle(self, *args, **options):
        created = 0
        for data in SAMPLE_POSTS:
            _, was_created = Post.objects.get_or_create(title=data["title"], defaults=data)
            created += int(was_created)
        self.stdout.write(
            self.style.SUCCESS(
                f"seed_posts: created {created} post(s), "
                f"{len(SAMPLE_POSTS) - created} already present."
            )
        )
