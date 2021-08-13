from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers
from research.views import ResearchViewSet, NoticeViewSet, AskViewSet

app_name = "research"

router = SimpleRouter()
router.register("", ResearchViewSet)

notice_router = routers.NestedSimpleRouter(router, r"", lookup="research")
notice_router.register(r"notice", NoticeViewSet, basename="research-notice")

ask_router = routers.NestedSimpleRouter(router, r"", lookup="research")
ask_router.register(r"ask", AskViewSet, basename="research-ask")

urlpatterns = []

urlpatterns += router.urls
urlpatterns += notice_router.urls
urlpatterns += ask_router.urls
