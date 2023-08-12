"""
Views for the user API.
"""

from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.authentication import TokenAuthentication
from .serializer import (
    UserSerializer,
    AuthTokenSerializer
)


class CreateUserView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, *args, **kwargs):
        data = request.data

        user_serializer = UserSerializer(data=data)

        if not user_serializer.is_valid():
            return Response(
                user_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
                )
        user = user_serializer.create(user_serializer.validated_data)
        user = UserSerializer(user)

        return Response(
            {'success': 'User created', 'data': user.data},
            status=status.HTTP_201_CREATED
            )


class CreateTokenView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        token_serializer = AuthTokenSerializer(
            data=request.data,
            context={'request': request}
            )
        token_serializer.is_valid(raise_exception=True)

        user = token_serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({'token': token.key}, status.HTTP_200_OK)


class ManagerUserView(APIView):

    authentication_classes = [TokenAuthentication]
    permissions_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return Response(
                {'detail': 'Not found.'},
                status=status.HTTP_401_UNAUTHORIZED
                )

        user_serializer = UserSerializer(user)

        return Response(user_serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        user = request.user
        user_serializer = UserSerializer(
            user,
            data=request.data,
            partial=True
            )

        if user_serializer.is_valid():
            user_serializer.save()
            return Response(
                user_serializer.data,
                status=status.HTTP_200_OK
                )
        else:
            return Response(
                user_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
                )
