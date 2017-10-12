from django.contrib.auth.models import User
from django.db import models


class Expense(models.Model):
    """
    Expense model with customizable date/category/type/value/currency values
    Defined by the date and user submitting the request
    """
    # TODO: implement default date to today
    date = models.DateField(blank=True, null=True)

    # TODO: hide this from expense response
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    category = models.CharField(max_length=32, blank=False, null=False)
    type = models.CharField(max_length=32, blank=False, null=False)
    value = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    # TODO: implement field not being required for POST
    currency = models.CharField(max_length=3, blank=True, null=True, default='CAD')
