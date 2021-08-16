from django.db.models import Q, Count

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

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
import datetime

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
            marked=Count("mark_users__id")
        ).order_by("marked")

        if keyword:
            search_result = search_result.filter(subject__iexact=keyword)
        if tags:
            search_result = search_result.filter(tags__tag_name__in=tags)
        if sort:
            search_result = search_result.order_by(sort)
        if pay:
            search_result = search_result.filter(reward__amount__gte=pay)
        if time_range:
            start = datetime(time_range[0], time_range[1], time_range[2], 0, 0)
            end = datetime(time_range[3], time_range[4], time_range[5], 0, 0)
            search_result = search_result.filter(research_start__range=(start, end))
            search_result = search_result.filter(research_end__range=(start, end))
        search_result = page.paginate_queryset(search_result, request)
        serializer = self.get_serializer(search_result, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)