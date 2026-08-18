from django.contrib import admin

from .models import Post
from .widgets import MarkdownPreviewWidget


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "is_published", "created_at", "updated_at")
    list_filter = ("is_published", "created_at")
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}  # slug autofill from title
    list_editable = ("is_published",)
    date_hierarchy = "created_at"
    formfield_overrides = {
        Post._meta.get_field("content").__class__: {"widget": MarkdownPreviewWidget},
    }
