import os

# 환경 변수 DJANGO_SETTINGS_MODULE의 값을 가져옴
SETTINGS_MODULE = os.environ.get("DJANGO_SETTINGS_MODULE")

# 환경 변수의 값이 None, "yeonguham.settings" 또는 "yeonguham.settings.dev"이면 dev.py 불러옴
if (
    not SETTINGS_MODULE
    or SETTINGS_MODULE == "yeonguham.settings"
    or SETTINGS_MODULE == "yeonguham.settings.dev"
):
    from .dev import *

# 환경 변수의 값이 "yeonguham.settings.local"이면 local.py 불러옴
elif SETTINGS_MODULE == "yeonguham.settings.local":
    from .local import *
