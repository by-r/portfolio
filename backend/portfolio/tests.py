from io import StringIO

import pytest
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.management import CommandError, call_command
from django.test import Client, override_settings
from ninja.testing import TestClient

from config.api import api
from portfolio.models import Post

client = TestClient(api)
django_client = Client()


@pytest.fixture
def posts(db):
    published = Post.objects.create(
        title="Hello World",
        slug="hello-world",
        content="# Hello\n\nSome **markdown**.",
        is_published=True,
    )
    Post.objects.create(title="Draft", slug="draft", content="secret", is_published=False)
    return published


def test_health_ok():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_list_posts_only_published(posts):
    resp = client.get("/posts")
    assert resp.status_code == 200
    body = resp.json()
    assert [p["slug"] for p in body] == ["hello-world"]
    assert "content" not in body[0]
    assert "excerpt" in body[0]


def test_list_newest_first(db):
    first = Post.objects.create(title="First", slug="first", content="a", is_published=True)
    second = Post.objects.create(title="Second", slug="second", content="b", is_published=True)
    Post.objects.filter(pk=first.pk).update(created_at="2024-01-01T00:00:00Z")
    Post.objects.filter(pk=second.pk).update(created_at="2025-01-01T00:00:00Z")
    body = client.get("/posts").json()
    assert [p["slug"] for p in body] == ["second", "first"]


def test_detail_returns_content(posts):
    resp = client.get("/posts/hello-world")
    assert resp.status_code == 200
    body = resp.json()
    assert body["title"] == "Hello World"
    assert "**markdown**" in body["content"]


def test_detail_draft_404(posts):
    resp = client.get("/posts/draft")
    assert resp.status_code == 404


def test_detail_unknown_slug_404(db):
    resp = client.get("/posts/nope")
    assert resp.status_code == 404


# --- Security -----------------------------------------------------------


def test_security_headers_present():
    resp = django_client.get("/api/health")
    assert resp.status_code == 200
    assert "Content-Security-Policy" in resp.headers
    assert resp.headers["X-Content-Type-Options"] == "nosniff"
    assert resp.headers["X-Frame-Options"] == "DENY"
    assert resp.headers["Referrer-Policy"] == "same-origin"


def test_cors_allows_frontend_origin():
    resp = django_client.get("/api/health", HTTP_ORIGIN="http://localhost:5173")
    assert resp.headers.get("Access-Control-Allow-Origin") == "http://localhost:5173"


def test_cors_rejects_foreign_origin():
    resp = django_client.get("/api/health", HTTP_ORIGIN="https://evil.example")
    assert "Access-Control-Allow-Origin" not in resp.headers


def test_admin_path_is_not_default():
    assert django_client.get("/admin/login/").status_code == 404
    assert django_client.get("/staff/login/").status_code == 200


def test_api_rate_limited():
    cache.clear()
    with override_settings(RATE_LIMIT_PER_MINUTE=2):
        assert django_client.get("/api/health").status_code == 200
        assert django_client.get("/api/health").status_code == 200
        assert django_client.get("/api/health").status_code == 429


def test_admin_login_throttled(db):
    cache.clear()
    with override_settings(ADMIN_LOGIN_LIMIT=2):
        for _ in range(2):
            resp = django_client.post("/staff/login/", {"username": "x", "password": "y"})
            assert resp.status_code in (200, 302)
        assert (
            django_client.post("/staff/login/", {"username": "x", "password": "y"}).status_code
            == 429
        )


def test_seed_demo_is_idempotent_and_authenticates(db):
    output = StringIO()
    with override_settings(DEBUG=True):
        call_command("seed_demo", stdout=output)
        Post.objects.filter(slug="welcome-to-my-portfolio").update(
            content="stale content", is_published=False
        )
        call_command("seed_demo", stdout=output)

    User = get_user_model()
    assert User.objects.filter(username="admin").count() == 1
    admin = User.objects.get(username="admin")
    assert admin.email == "admin@example.test"
    assert admin.is_superuser
    credentials = {"username": "admin", "pass" + "word": "admin"}
    assert Client().login(**credentials)

    assert Post.objects.count() == 2
    assert Post.objects.filter(is_published=True).count() == 2
    welcome = Post.objects.get(slug="welcome-to-my-portfolio")
    assert welcome.is_published
    assert welcome.content != "stale content"
    assert set(Post.objects.values_list("slug", flat=True)) == {
        "welcome-to-my-portfolio",
        "building-this-site",
    }
    assert "development/demo use only" in output.getvalue()


def test_seed_demo_rejects_production(db):
    with pytest.raises(CommandError, match="only available when DEBUG=True"):
        call_command("seed_demo")

    assert not get_user_model().objects.filter(username="admin").exists()
    assert not Post.objects.exists()
