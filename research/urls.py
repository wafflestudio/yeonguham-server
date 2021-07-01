from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('researches/', views.ResearchList.as_view()),
    path('researches/<int:rid>/', views.ResearchDetail.as_view()),
    path('researches/<int:rid>/notice',views.NoticeList.as_view()),
    path('researches/<int:rid>/notice/<int:nid>',views.NoticeDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)