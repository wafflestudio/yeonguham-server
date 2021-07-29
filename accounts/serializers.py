from django.contrib.auth.models import User
from rest_framework import serializers

from accounts.models import ProxyUser


class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
    interests = serializers.ListField(child=serializers.CharField())

    def create(self, validated_data):
        return ProxyUser.objects.create_user_and_profile(
            username=validated_data.get("username"),
            email=validated_data.get("email"),
            access_token=validated_data.get("access_token"),
            refresh_token=validated_data.get("refresh_token"),
            interests=validated_data.get("interests"),
        )

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("이미 존재하는 이메일입니다.")
        return value
