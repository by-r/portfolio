"""Django settings for the portfolio project.

All secrets and environment-specific values come from the environment
(backend/.env or the repo-root .env). See backend/.env.example for the
full list of variables. Never commit real secrets.
"""

from pathlib import Path

from django.core.exceptions import ImproperlyConfigured
from environs import Env

BASE_DIR = Path(__file__).resolve().parent.parent

env = Env()
env.read_env(BASE_DIR / ".env", recurse=False)
env.read_env(BASE_DIR.parent / ".env", recurse=False)

# ---------------------------------------------------------------------------
# Core
# ---------------------------------------------------------------------------
SECRET_KEY = env("SECRET_KEY", default="dev-insecure-secret-key-change-me")
DEBUG = env.bool("DEBUG", default=False)
if not DEBUG and SECRET_KEY == "dev-insecure-secret-key-change-me":
    raise ImproperlyConfigured("SECRET_KEY must be set to a real value when DEBUG=False.")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "csp",
    "portfolio",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "portfolio.middleware.RateLimitMiddleware",
    "csp.middleware.CSPMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# ---------------------------------------------------------------------------
# Database — SQLite by default, PostgreSQL via DATABASE_URL
# ---------------------------------------------------------------------------
DATABASE_URL = env("DATABASE_URL", default="")
if DATABASE_URL:
    from urllib.parse import urlparse

    url = urlparse(DATABASE_URL)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": url.path[1:],
            "USER": url.username,
            "PASSWORD": url.password,
            "HOST": url.hostname,
            "PORT": url.port or 5432,
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------------------------------------------------------
# Security
# ---------------------------------------------------------------------------
# CORS — only the frontend origin(s) may call the API cross-origin.
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=["http://localhost:5173"])
CORS_ALLOW_METHODS = ("GET", "HEAD", "OPTIONS")
CORS_ALLOW_CREDENTIALS = False

# HTTPS / secure cookies — flip HTTPS=True in production behind TLS.
HTTPS = env.bool("HTTPS", default=False)
SESSION_COOKIE_SECURE = HTTPS
CSRF_COOKIE_SECURE = HTTPS
SECURE_SSL_REDIRECT = HTTPS
SECURE_HSTS_SECONDS = env.int("SECURE_HSTS_SECONDS", default=0)
SECURE_HSTS_INCLUDE_SUBDOMAINS = HTTPS
SECURE_HSTS_PRELOAD = HTTPS
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"
X_FRAME_OPTIONS = "DENY"

# Content-Security-Policy (django-csp 4.x). Inline styles are required by the
# Django admin; scripts/images/fonts come from self only.
CSP_DIRECTIVES = {
    "default-src": ("'self'",),
    "style-src": ("'self'", "'unsafe-inline'"),
    "script-src": ("'self'",),
    "img-src": ("'self'", "data:"),
    "font-src": ("'self'",),
    "connect-src": ("'self'",),
    "frame-ancestors": ("'none'",),
    "form-action": ("'self'",),
}

# The ninja OpenAPI docs page loads Swagger UI from a CDN — only in dev.
if DEBUG:
    for directive in ("script-src", "style-src", "img-src", "font-src", "connect-src"):
        CSP_DIRECTIVES[directive] += ("https://cdn.jsdelivr.net", "https://unpkg.com")

CONTENT_SECURITY_POLICY = {"DIRECTIVES": CSP_DIRECTIVES}

# Admin URL — non-default path (reduces attack surface/noise), env-configurable.
ADMIN_URL = env("ADMIN_URL", default="staff/")

# API rate limit (requests per minute per IP). Uses the default cache — use a
# shared cache (e.g. Redis) in production for accurate limits across workers.
RATE_LIMIT_PER_MINUTE = env.int("RATE_LIMIT_PER_MINUTE", default=120)
# Only enable when behind a trusted reverse proxy that sets X-Forwarded-For.
RATE_LIMIT_TRUST_PROXY = env.bool("RATE_LIMIT_TRUST_PROXY", default=False)
