from rest_framework import serializers
from .models import Research, Notice, Ask


class ResearchSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True)
    mark_users = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    researchees = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

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
        ]


class HotResearchSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True)

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
    tags = serializers.StringRelatedField(many=True)

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


class AskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ask
        fields = ["id", "research", "asker", "content", "private"]
