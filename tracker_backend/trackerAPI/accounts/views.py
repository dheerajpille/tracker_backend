from django.shortcuts import render
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

class UserList(ListAPIView):

    # Only gives admin permission to view user list
    permission_classes = {IsAdminUser, }
    pagination_class = None
    authentication_classes = {JSONWebTokenAuthentication, }
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('id')