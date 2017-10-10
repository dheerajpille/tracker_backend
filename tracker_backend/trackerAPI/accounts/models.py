from django.db import models
from django.contrib.auth.models import AbstractUser

from django.utils.timezone import now


# Create your models here.
class User(AbstractUser):
    """
    Custom user model with additional (monthly) budget and currency parameter
    """
    budget = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
