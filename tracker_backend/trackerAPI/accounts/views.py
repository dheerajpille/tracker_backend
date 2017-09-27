from django.shortcuts import render
from rest_framework import status
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer, LoginSerializer

# Create your views here.
class LoginView(APIView):
    def post(self, request):
        validate_user = LoginSerializer(data=request.data)

        if validate_user.is_valid():
            serializer = UserSerializer(validate_user.validated_data, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(validate_user.errors, status=status.HTTP_401_UNAUTHORIZED)