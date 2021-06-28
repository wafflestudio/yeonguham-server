from rest_framework import serializers


class ResearchSerializer(serializers.ModelSerializer):
    researcher = serializers.PrimaryKeyRelatedField()
    tag = serializers.StringRelatedField(many=True)
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
            "resarch_end",
            "detail",
            "requirement",
            "capacity",
            "current_number",
            "hit",
            "reseacher",
            "tag",
            "mark_users",
            "researchees",
            "status",
        ]
