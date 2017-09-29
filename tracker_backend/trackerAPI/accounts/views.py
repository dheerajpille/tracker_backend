from django.shortcuts import render
from django.http import Http404
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import User
from .serializers import *


# Create your views here.
class LoginView(APIView):

    # Gives any user permission to POST for login
    permission_classes = {AllowAny, }

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
        user = self.get_object(pk)
        if request.user.is_superuser or request.user == user:
            user = self.get_object(pk)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(data={"message": "Not authorized to delete this user."}, status=status.HTTP_401_UNAUTHORIZED)

class UserList(ListAPIView):

    # Disables pagination for GET calls
    pagination_class = None
    serializer_class = UserSerializer

    def get(self, request):
        user = self.get_object(pk)
        if request.user.is_superuser or request.user == user:
            queryset = User.objects.all().order_by('id')
        else:
            return Response(data={"message": "Not authorized to view the user list."}, status=status.HTTP_401_UNAUTHORIZED)