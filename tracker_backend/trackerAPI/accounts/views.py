from django.shortcuts import render
from django.http import Http404
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import User
from .serializers import *

# Create your views here.
class LoginView(APIView):

    # Gives any user permission to POST for login
    permission_classes = {AllowAny, }
    authentication_classes = (JSONWebTokenAuthentication, )

    def post(self, request):
        validate_user = LoginSerializer(data=request.data)

        if validate_user.is_valid():
            serializer = UserSerializer(validate_user.validated_data, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(validate_user.errors, status=status.HTTP_401_UNAUTHORIZED)

class SignupView(APIView):

    # Gives any user permission to POST for signup
    permission_classes = {AllowAny, }

    def post(self, request):
        create_user = SignupSerializer(data=request.data)

        if create_user.is_valid():
            create_user.save()
            serializer = UserSerializer(create_user.data, context={'request': request})

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(create_user.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetail(APIView):

    # TODO: delete if not needed (most likely)
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        if request.user == user:
            serializer = UserSerializer(user, context={'request', request})
            return Response(serializer.data)
        else:
            return Response(data={"message": "Not authorized to view this user."}, status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, pk):
        user = self.get_object(pk)
        if request.user == user:
            serializer = UserSerializer(user, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()

                return Response(serializer.data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(data={"message": "Not authorized to edit this user."}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, pk):
        if self.request.user.is_superuser or self.request.user.pk == int(pk):
            user = self.get_object(pk)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(data={"message": "Not authorized to delete this user."}, status=status.HTTP_401_UNAUTHORIZED)

class UserList(ListAPIView):

    # Only gives admin permission to view user list
    permission_classes = {IsAdminUser, }

    # Disables pagination for GET calls
    pagination_class = None
    authentication_classes = {JSONWebTokenAuthentication, }
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('id')