from rest_framework import serializers
from .models import Research, Tag, Notice, Ask, Answer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["tag_name"]


class ResearchSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    mark_users = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    researchees = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    rewards = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Research
        fields = [
            "id",
            "subject",
            "create_date",
            "update_date",
            "recruit_start",
            "recruit_end",
            "research_start",
            "research_end",
            "link",
            "detail",
            "requirement",
            "capacity",
            "current_number",
            "hit",
            "researcher",
            "tags",
            "mark_users",
            "researchees",
            "rewards",
        ]


class HotResearchSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Research
        fields = [
            "id",
            "subject",
            "recruit_end",
            "capacity",
            "current_number",
            "tags",
            "status",
        ]


class NewResearchSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Research
        fields = [
            "id",
            "subject",
            "recruit_start",
            "recruit_end",
            "current_number",
            "capacity",
            "tags",
        ]


class RecommendResearchSerialzier(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Research
        fields = [
            "id",
            "subject",
            "recruit_start",
            "recruit_end",
            "capacity",
            "current_number",
            "hit",
            "status",
            "tags",
        ]


class NoticeSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ["id", "research", "title", "body", "image"]


class NoticeSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ["id", "title", "image"]


class NoticeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ["title", "body", "image"]


class AskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ask
        fields = ["id", "research", "asker", "content", "private"]


class AskSimpleSerializer(serializers.ModelSerializer):
    asker = serializers.ReadOnlyField(source="asker.researchee.nickname")

    class Meta:
        model = Ask
        fields = ["id", "asker", "content"]


class AskDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ask
        fields = ["content", "private", "asker"]


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ["id", "ask", "content"]
