from rest_framework import serializers
from . import Research, Notice


class ResearchSerialzier(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True)
    mark_users = serializers.PrimaryKeyRelatedField(many=True)
    researchees = serializers.PrimaryKeyRelatedField(many=True)

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


class NoticeSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ["id", "research", "title", "body", "image"]
