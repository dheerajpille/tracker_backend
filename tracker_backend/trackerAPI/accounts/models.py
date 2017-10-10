from django.db import models
from django.contrib.auth.models import AbstractUser

from django.utils.timezone import now


# Create your models here.
class User(AbstractUser):
    """
    Custom user model with additional (monthly) budget and currency parameter
    """
    budget = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)


class Expense(models.Model):
    """
    Expense model with customizable category/type/value/currency values
    Defined by the date and user submitting the request
    """
    # TODO: figure out how to implement default date to today
    date = models.DateField(blank=True, null=True, default=now().date())

    # TODO: hide this from expense response
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    category = models.CharField(max_length=32, blank=False, null=False)
    type = models.CharField(max_length=32, blank=False, null=False)
    value = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, blank=True, null=True, default='CAD')
