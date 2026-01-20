import os

import dj_database_url

from .base import *

if not os.environ.get("DJANGO_SECRET_KEY"):
    raise RuntimeError("DJANGO_SECRET_KEY is required when using ll_project.settings.prod")

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
DJANGO_SETTINGS_MODULE=os.environ["DJANGO_SETTINGS_MODULE"]
DEBUG = env_bool("DJANGO_DEBUG", default=False)
ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS", default=[])

# Static files (prod)
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

# Database (prod)
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases
DATABASES = {
    "default": dj_database_url.config(
        default=None,
        conn_max_age=600,
        ssl_require=True,
    )
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]