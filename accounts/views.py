from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView

from accounts.serializers import UserCreateSerializer


class UserCreateView(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()  # UserCreateSerializer.create 호출
        return Response(data=user.pk, status=HTTP_201_CREATED)
