from django.conf import settings
from django.contrib import admin
from django.urls import path

from config.api import api

urlpatterns = [
    # Non-default, env-configurable admin path (settings.ADMIN_URL).
    path(settings.ADMIN_URL, admin.site.urls),
    path("api/", api.urls),
]
