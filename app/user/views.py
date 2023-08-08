"""
Views for the user API.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .serializer import UserSerializer


class CreateUserView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, *args, **kwargs):
        data = request.data

        serializer = UserSerializer(data=data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
                )
        user = serializer.create(serializer.validated_data)
        user = UserSerializer(user)

        return Response(
            {'success': 'User created', 'data': user.data},
            status=status.HTTP_201_CREATED
            )
