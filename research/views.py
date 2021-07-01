from . import (
    Research,
    Tag,
    Reward,
    ResearcheeResearch,
    TagResearch,
    Notice,
    Mark,
    Answer,
)
from . import (
    ResearchSerializer,
    HotResearchSerializer,
    NewResearchSerializer,
    NoticeSerializer,
)
from rest_framework.views import APIView, status
from rest_framework.response import Response
from django.http import Http404

# Create your views here.


class ReserachList(APIView):
    def get(self, request):
        researches = Research.objects.all()
        for research in researches:
            research.get_status()
        researches = Research.objects.all().excldue(status="EXP")
        serializer = HotResearchSerializer(researches, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ResearchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResearchDetail(APIView):
    def get_object(self, rid):
        try:
            return Research.objects.get(pk=rid)
        except Research.DoesNotExist:
            raise Http404

    def get(self, request, rid):
        research = self.get_object(rid)
        serializer = ResearchSerializer(research)
        return Response(serializer.data)

    def put(self, request, rid):
        research = self.get_object(rid)
        serializer = ResearchSerializer(research, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, rid):
        research = self.get_object(rid)
        research.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class NoticeList(APIView):
    def get(self, request, rid):
        notices = Notice.objects.filter(research__id=rid)
        serializer = NoticeSerializer(notices, many=True)
        return Response(serializer.data)

    def post(self, request, rid):
        serializer = NoticeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
