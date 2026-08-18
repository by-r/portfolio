from datetime import datetime

from django.shortcuts import get_object_or_404
from ninja import Router, Schema

from .models import Post

router = Router(tags=["posts"])


class PostSummary(Schema):
    title: str
    slug: str
    excerpt: str
    created_at: datetime
    updated_at: datetime


class PostDetail(PostSummary):
    content: str


@router.get("/posts", response=list[PostSummary], summary="List published posts")
def list_posts(request):
    """Published posts, newest first."""
    return Post.objects.filter(is_published=True)


@router.get("/posts/{slug}", response=PostDetail, summary="Get a single post")
def get_post(request, slug: str):
    """A single published post by slug; 404 for drafts or unknown slugs."""
    return get_object_or_404(Post, slug=slug, is_published=True)
