import re

from django.db import models
from django.utils.text import slugify


class Post(models.Model):
    """A blog post. Content is authored as Markdown in Django admin."""

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    content = models.TextField(help_text="Markdown is supported.")
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    @property
    def excerpt(self) -> str:
        """A short plain-text preview of the Markdown body."""
        text = re.sub(r"[#>*_`~\[\]()!\\-]", " ", self.content)
        text = re.sub(r"\s+", " ", text).strip()
        return text[:160] + ("…" if len(text) > 160 else "")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
