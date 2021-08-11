from django.urls import include, path
from rest_framework.routers import SimpleRouter
from .views import SearchViewSet

app_name = "search"

router = SimpleRouter()
router.register("", SearchViewSet, basename="search")

urlpatterns = [path("", include((router.urls)))]
