import requests
import os
import json
import base64

from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import render

# Create your views here.