from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from accounts.serializers import UserCreateSerializer
from accounts.models import Profile


class UserViewSet(viewsets.GenericViewSet):
    queryset = Profile.objects.all()
    permission_classes = (IsAuthenticated(),)

    def get_serializer_class(self):
        return UserCreateSerializer

    def create(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request, user)
        return Response(data=user.pk, status=status.HTTP_201_CREATED)