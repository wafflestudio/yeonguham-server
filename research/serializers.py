from rest_framework import serializers
from .models import Research, Tag, Notice, Ask, Answer, Reward


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "tag_name"]


class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = ["id", "reward_type", "amount"]


class SimpleResearchCreateSerializer(serializers.ModelSerializer):
    create_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    update_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    recruit_start = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    recruit_end = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    research_start = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    research_end = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

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
            "images",
            "location",
            "researcher",
        ]

    def create(self, research):
        return Research.objects.create(**research)


class ResearchCreateSerializer(SimpleResearchCreateSerializer):
    reward = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Research
        fields = SimpleResearchCreateSerializer.Meta.fields + ["reward", "tags"]

    def get_reward(self, research):
        reward = research.reward
        return RewardSerializer(reward).data

    def get_tags(self, research):
        tags = research.tags
        return TagSerializer(tags, many=True).data

    # def get_researcher(self,research):
    #     return ProfileSerializer()


class ResearchViewSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    reward = serializers.SerializerMethodField()

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
            "reward",
            "link",
            "detail",
            "requirement",
            "capacity",
            "current_number",
            "researcher",
            "tags",
            "hit",
            "location",
            "images",
        ]

    def get_tags(self, research):
        return TagSerializer(research.tags.all(), many=True)

    def get_reward(self, research):
        return RewardSerializer(research.reward).save()


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
            "images",
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


class RecommendResearchSerializer(serializers.ModelSerializer):
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


class SimpleResearchSerializer(serializers.ModelSerializer):
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
            "tags",
        ]


class NoticeCreateSerializer(serializers.ModelSerializer):
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
        fields = ["id", "title", "body", "image"]


class AskCreateSerializer(serializers.ModelSerializer):
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
