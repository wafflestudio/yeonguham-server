import os
import json
import sys

from base import *

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS += []

WSGI_APPLICATION = "yeonguham.wsgi.local.application"

SECRETS_FILE = os.path.join(BASE_DIR, "secrets-local.json")

secrets = json.loads(open(SECRETS_FILE).read())
for key, value in secrets.items():
    setattr(sys.modules[__name__], key, value)
