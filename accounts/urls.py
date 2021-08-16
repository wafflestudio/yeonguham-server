from django.urls import path, include 
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import SimpleRouter
from accounts.views import UserViewSet

app_name = "accounts"

router = SimpleRouter()
router.register("", UserViewSet)

urlpatterns = []

urlpatterns += router.urls
