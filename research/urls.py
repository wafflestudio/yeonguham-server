from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path("", views.ResearchList.as_view()),
    path("<int:rid>/", views.ResearchDetail.as_view()),
    path("<int:rid>/notice/", views.NoticeList.as_view()),
    path("<int:rid>/notice/<int:nid>/", views.NoticeDetail.as_view()),
    path("<int:rid>/ask/", views.AskList.as_view()),
    path("<int:rid>/ask/<int:aid>/", views.AskDetail.as_view()),
    path("search/", views.SearchList.as_view()),
    path("field", views.FieldList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
