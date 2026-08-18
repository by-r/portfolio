from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse

# Admin login attempts per minute per IP (credential-stuffing surface).
ADMIN_LOGIN_LIMIT = 10


class RateLimitMiddleware:
    """Simple per-IP rate limiting using the Django cache.

    - Public API (``/api/*``, GET/HEAD): ``RATE_LIMIT_PER_MINUTE``/min
    - Admin login (``POST <ADMIN_URL>login/``): ``ADMIN_LOGIN_LIMIT``/min

    Use a shared cache (e.g. Redis) in production so the limit is accurate
    across workers; the default LocMemCache is per-process only.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method not in ("GET", "HEAD", "POST"):
            return self.get_response(request)

        limit = None
        if request.path.startswith("/api/"):
            limit = getattr(settings, "RATE_LIMIT_PER_MINUTE", 120)
        elif request.method == "POST" and request.path == (
            "/" + getattr(settings, "ADMIN_URL", "staff/").lstrip("/") + "login/"
        ):
            limit = getattr(settings, "ADMIN_LOGIN_LIMIT", ADMIN_LOGIN_LIMIT)

        if limit is not None and self._over_limit(request, limit):
            return HttpResponse("Too Many Requests", status=429)
        return self.get_response(request)

    @staticmethod
    def _over_limit(request, limit: int) -> bool:
        area = request.path.split("/")[1] or "root"
        key = f"ratelimit:{area}:{RateLimitMiddleware._client_ip(request)}"
        # cache.add is atomic: first request in the window sets count=1.
        if cache.add(key, 1, timeout=60):
            return 1 > limit
        try:
            count = cache.incr(key)
        except ValueError:
            return False  # key expired between add and incr — let it pass
        return count > limit

    @staticmethod
    def _client_ip(request):
        # Only trust X-Forwarded-For when explicitly enabled AND the reverse
        # proxy is known to overwrite (never append to) that header — otherwise
        # a client-supplied value lets attackers rotate their own limit key.
        if getattr(settings, "RATE_LIMIT_TRUST_PROXY", False):
            forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
            if forwarded:
                return forwarded.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR", "unknown")
