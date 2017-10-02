from django.db import models
from django.contrib.auth.models import AbstractUser
from oauth2_provider.models import RefreshToken
from rest_framework.authtoken.models import Token

# Create your models here.
class User(AbstractUser):
    budget = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

class Bearer:
    def __init__(self, tokenType, accessToken, refreshToken, accessTokenExpiry, refreshTokenExpiry, idToken=None):
        self.tokenType = tokenType
        self.accessToken = accessToken
        self.refreshToken = refreshToken
        self.accessTokenExpiry = accessTokenExpiry
        self.refreshTokenExpiry = refreshTokenExpiry
        self.idToken = idToken
