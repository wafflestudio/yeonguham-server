from django.db.models import Q, Count

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from accounts.models import Profile
from research.models import (
    Research,
    Tag,
    Reward,
    ResearcheeResearch,
    TagResearch,
    Notice,
    Mark,
    Ask,
    Answer,
)
from research.serializers import SimpleResearchSerializer
from research.pagination import ListPagination
from datetime import datetime

# Create your views here.


class SearchViewSet(viewsets.GenericViewSet):
    queryset = Research.objects.annotate(count=Count("mark_users")).order_by("count")
    serializer_class = SimpleResearchSerializer

    def list(self, request):
        keyword = request.query_params.get("query")
        tags = request.query_params.get("tags")
        sort = request.query_params.get("sort")
        pay = request.query_params.get("pay")
        time_range = request.query_params.get("time_range")
        page = ListPagination()

        search_result = Research.objects.annotate(
            marked=Count("mark_users")
        ).order_by("marked")

        q = Q()

        if keyword:
            q.add(
                Q(subject__icontains=keyword) | Q(researcher__name__icontains=keyword),
                q.AND,
            )
        if tags:
            q.add(Q(tags__tag_name__in=tags), q.AND)
        if pay:
            q.add(Q(reward__amount__gte=pay), q.AND)
        if time_range:
            start = datetime.striptime(time_range[0], "%Y-%m-%d %H:%M:%S")
            end = datetime.striptime(time_range[1], "%Y-%m-%d %H:%M:%S")
            q.add(
                Q(research_start__range=(start, end))
                & Q(research_end__range=(start, end)),
                q.AND,
            )

        search_result.filter(q).distinct()
        if sort:
            search_result = search_result.order_by(sort)
        search_result = page.paginate_queryset(search_result, request)
        serializer = self.get_serializer(search_result, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
