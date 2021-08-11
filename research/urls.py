from django.urls import path, include
from rest_framework.routers import SimpleRouter
from research.views import ResearchViewSet, NoticeViewSet, AskViewSet

app_name = 'research'

router = SimpleRouter()
router.register(r"notice", NoticeViewSet, basename= "research")
router.register(r"ask",AskViewSet, basename= "research")
router.register("", ResearchViewSet, basename="research")  

urlpatterns = [
   
]

urlpatterns += router.urls