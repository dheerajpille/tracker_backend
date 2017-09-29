from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    budget = models.DecimalField(max_digits=    8, decimal_places=2, blank=True, null=True)