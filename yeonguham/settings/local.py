import json
import sys

from .base import *

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS += []

WSGI_APPLICATION = "yeonguham.wsgi.local.application"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django.db.backends": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
    },
}

SECRETS_FILE = os.path.join(BASE_DIR, "secrets-local.json")

secrets = json.loads(open(SECRETS_FILE).read())
for key, value in secrets.items():
    setattr(sys.modules[__name__], key, value)
