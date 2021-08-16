from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt, action

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from accounts.serializers import UserCreateSerializer


class UserViewSet(viewsets.GenericViewSet):
    queryset = Profile.objects.all()
    permission_classes = (IsAuthenticated(),)

    def get_serialzier_class(self):
        return UserCreateSerializer

    def create(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request, user)
        return Response(data=user.pk, status=HTTP_201_CREATED)        