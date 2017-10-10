from django.shortcuts import render
from django.http import Http404, HttpResponse
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import *
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from django.utils.timezone import now

from django.contrib.auth.models import User
from tracker_backend.trackerAPI.accounts.serializers import UserSerializer
from tracker_backend.trackerAPI.serializers import LoginSerializer, SignupSerializer

# Create your views here.
class LoginView(APIView):
    """
    Allows client to login with user credentials (username/password)
    """

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
    """
    Allows client to signup with user credentials (username/email/password)
    Other fields are optional
    """

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