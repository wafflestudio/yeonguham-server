from django.urls import path, include
from rest_framework.routers import SimpleRouter
from research.views import ResearchViewSet, NoticeViewSet, AskViewSet

app_name = 'research'

router = SimpleRouter()
router.register("", ResearchViewSet, basename="research")  

urlpatterns = [
    path("<int:rid>/notice/", NoticeViewSet.as_view()),
    path("<int:rid>/ask/", AskViewSet.as_view()),
]

urlpatterns += router.urls