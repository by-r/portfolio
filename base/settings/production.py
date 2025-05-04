from .base import *
from pathlib import Path
import os

from base.settings import get_secret
from django.core.management.utils import get_random_secret_key

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_secret("SECRET_KEY", get_random_secret_key())
DEBUG = bool(os.environ.get("DEBUG", False))

ALLOWED_HOSTS = ["*"]
