from django.conf.urls import url, include
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from tracker_backend.trackerAPI.accounts.views import *

urlpatterns = [
    # Add any URLs if needed
]