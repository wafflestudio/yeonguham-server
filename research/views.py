from .models import (
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
from .serializers import (
    TagSerializer,
    RewardSerializer,
    SimpleResearchCreateSerializer,
    ResearchCreateSerializer,
    ResearchViewSerializer,
    HotResearchSerializer,
    NewResearchSerializer,
    RecommendResearchSerializer,
    SimpleResearchSerializer,
    NoticeCreateSerializer,
    NoticeSimpleSerializer,
    NoticeDetailSerializer,
    AskCreateSerializer,
    AskSimpleSerializer,
    AskDetailSerializer,
    AnswerSerializer,
)
from .pagination import ListPagination, NoticePagination, AskPagination
from rest_framework import viewsets
from rest_framework.views import APIView, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.http import Http404
from django.db import transaction
from datetime import datetime


class ResearchViewSet(viewsets.GenericViewSet):
    queryset = Research.objects.filter(recruit_end__gt=datetime.now())

    def get_permissions(self):
        return (AllowAny(),)

    def get_object(self, rid):
        try:
            return Research.objects.get(pk=rid)
        except Research.DoesNotExist:
            raise Http404

    def list(self, request):
        researches = Research.objects.filter(recruit_end__gt=datetime.now())
        hot_researches = researches[:24]
        hot_serializer = HotResearchSerializer(hot_researches, many=True)
        new_researches = researches.order_by("-create_date")[:24]
        new_serializer = NewResearchSerializer(new_researches, many=True)
        context = {
            "hot_research": hot_serializer.data,
            "new_research": new_serializer.data,
        }
        return Response(context)

    def create(self, request):
        data = request.data.copy()
        reward = data.pop("reward")
        tags = data.pop("tags")
        serializer = SimpleResearchCreateSerializer(data=data, files=request.FILES)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            research = serializer.save(researcher=request.user.profile)

            Reward.objects.create(
                research=research,
                reward_type=reward.get("reward_type"),
                amount=reward.get("amount"),
            )
        for tag_name in tags:
            field_tag = {"tag_name": tag_name}
            try:
                tag = Tag.objects.get(tag_name=tag_name)
            except Tag.DoesNotExist:
                tag_serializer = TagSerializer(data=field_tag)
                tag_serializer.is_valid(raise_exception=True)
                tag = tag_serializer.save()

            with transaction.atomic():
                if TagResearch.objects.filter(research=research, tag=tag).exists():
                    return Response(
                        {"error": "중복된 tag입니다."},
                        status=status.HTTP_409_CONFLICT,
                    )
                TagResearch.objects.create(research=research, tag=tag)
        return Response(
            ResearchCreateSerializer(research).data, status=status.HTTP_201_CREATED
        )

    def retrieve(self, request, rid):
        research = self.get_object(rid)
        research.hit += 1
        research.save()
        serializer = ResearchViewSerializer(research)
        return Response(serializer.data)

    @action(detail=True, methods=["POST"])
    def participate(self, request, rid):
        research = self.get_object(rid)
        researchee = request.user.researchee
        try:
            already = ResearcheeResearch.objects(
                research=research, researchee=researchee
            )
        except ResearcheeResearch.DoesNotExist:
            ResearcheeResearch.objects.create(research=research, researchee=researchee)
            return Response(status=status.HTTP_201_CREATED)
        return Response({"error": "이미 참여하고 있는 연구입니다."}, status=status.HTTP_409_CONFLICT)

    def update(self, request, rid):
        research = self.get_object(rid)
        data = request.data.copy()
        updated_reward = data.pop("reward")
        updated_tags = data.pop("tags")

        try:
            reward = Reward.objects.filter(research=research)
            serializer = RewardSerializer(reward, data=updated_reward)
            serializer.is_valid(raise_exception=True)
            reward = serializer.save()
        except Reward.DoesNotExist:
            serializer = RewardSerializer(data=reward)
            serializer.is_valid(raise_exception=True)
            reward = serializer.save()

        old_tags = TagResearch.objects.filter(research=research)
        for tag_name in updated_tags:
            try:
                tag = Tag.objects.get(tag_name=tag_name)
            except Tag.DoesNotExist:
                tag = Tag.objects.create(tag_name=tag_name)

            if old_tags.filter(tag__tag_name=tag_name).exists():
                old_tags.exclude(tag__tag_name=tag_name)
            else:
                TagResearch.objects.create(research=research, tag=tag)
        for old_tag in old_tags:
            old_tag.delete()

        return Response(
            ResearchCreateSerializer(research).data, status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["PATCH"])
    def mark(self, request, rid):
        research = self.get_object(rid)
        try:
            mark = Mark.objects.get(user=request.user.profile, research=research)
            mark.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Mark.DoesNotExist:
            Mark.objects.create(user=request.user.profile, research=research)
        return Response(status=status.HTTP_200_OK)

    def destroy(self, request, rid):
        research = self.get_object(rid)
        research.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class NoticeViewSet(viewsets.GenericViewSet):
    queryset = Notice.objects.all()

    def get_object(self, nid):
        try:
            return Notice.objects.get(pk=nid)
        except Research.DoesNotExist:
            raise Http404

    def list(self, request, rid):
        notices = queryset.filter(research__id=rid)
        page = NoticePagination()
        notices = page.paginate_queryset(notices, request)
        serializer = NoticeSimpleSerializer(notices, many=True)
        return Response(serializer.data)

    def create(self, request, rid):
        serializer = NoticeCreateSerializer(data=request.data)
        research = Research.objects.get(id=rid)
        if serializer.is_valid():
            serializer.save(research=research)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, rid, nid):
        notice = self.get_object(nid)
        serializer = NoticeDetailSerializer(notice)
        return Response(serializer.data)

    def destroy(self, request, rid, nid):
        notice = self.get_object(nid)
        notice.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AskViewSet(viewsets.GenericViewSet):
    queryset = Ask.objects.all()

    def get_object(self, aid):
        try:
            return Ask.objects.get(pk=aid)
        except Research.DoesNotExist:
            raise Http404

    def list(self, request, rid):
        asks = Ask.objects.filter(research__id=rid)
        page = AskPagination()
        asks = page.paginate_queryset(asks, request)
        serializer = AskSimpleSerializer(asks, many=True)
        return Response(serializer.data)

    def create(self, request, rid):
        serializer = AskCreateSerializer(
            request.data  # , context=self.get_serializer_context()
        )
        research = Research.objects.get(id=rid)
        asker = request.user.profile
        if serializer.is_valid():
            serializer.save(research=research, asker=asker)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, rid, aid):
        ask = self.get_object(aid)
        serializer = AskDetailSerializer(ask)
        try:
            answer_set = Answer.objects.filter(ask=ask)
            answer = AnswerSerializer(answer_set, many=True).data
        except Answer.DoesNotExist:
            answer = {}
        context = {
            "ask": serializer.data,
            "answer": answer,
        }
        return Response(context)

    @action(detail == True, methods=["POST"])
    def answer(self, request, rid, aid):
        ask = self.get_object(aid)
        serializer = AnswerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        answer = serializer.save(ask=ask)
        return Response(answer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, rid, aid):
        ask = Ask.objects.get(pk=aid)
        ask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecommendList(APIView):
    def get(self, request):
        interests = request.user.researchee.interests
        sort = request.query_params.get("sort")
        page = ListPagination()
        recommendations = Research.objects.filter(
            tags__tag_name__in=interests
        ).order_by(sort)
        recommendations = page.paginate_queryset(recommendations, request)
        serializer = RecommendResearchSerializer(recommendations, many=True)
        return Response(serializer.data)
