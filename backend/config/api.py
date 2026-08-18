from django.conf import settings
from ninja import NinjaAPI

from portfolio.api import router as posts_router

api = NinjaAPI(
    title="Portfolio API",
    version="1.0.0",
    description="Read-only API powering the portfolio frontend.",
    # API schema/docs only in development; not exposed in production.
    docs_url="/docs" if settings.DEBUG else None,
)

api.add_router("/", posts_router)


@api.get("/health", tags=["system"], summary="Liveness probe")
def health(request):
    return {"status": "ok"}
