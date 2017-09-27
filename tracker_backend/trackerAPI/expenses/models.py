from django.db import models
from django.contrib.auth import get_user_model

from datetime import date

# Create your models here.
class Food(models.Model):
    """
    Food model, containing restaurant and groceries expense data
    """
    restaurant = models.DecimalField(max_digits=8, decimal_places=2)
    groceries = models.DecimalField(max_digits=8, decimal_places=2)

class Housing(models.Model):
    """
    Housing model, containing housing and rent expense data
    """
    housing = models.DecimalField(max_digits=8, decimal_places=2)
    rent = models.DecimalField(max_digits=8, decimal_places=2)

class Utilities(models.Model):
    """
    Utilities model, containing hydro, electricity, gas, internet, mobile, and television expense data
    """
    hydro = models.DecimalField(max_digits=8, decimal_places=2)
    electricity = models.DecimalField(max_digits=8, decimal_places=2)
    gas = models.DecimalField(max_digits=8, decimal_places=2)
    internet = models.DecimalField(max_digits=8, decimal_places=2)
    mobile = models.DecimalField(max_digits=8, decimal_places=2)
    television = models.DecimalField(max_digits=8, decimal_places=2)

class Transportation(models.Model):
    """
    Transportation model, containing fuel, parking, and public expense data
    """
    fuel = models.DecimalField(max_digits=8, decimal_places=2)
    parking = models.DecimalField(max_digits=8, decimal_places=2)
    public = models.DecimalField(max_digits=8, decimal_places=2)

class Insurance(models.Model):
    """
    Insurance model, containing health, household, and car expense data
    """
    health = models.DecimalField(max_digits=8, decimal_places=2)
    household = models.DecimalField(max_digits=8, decimal_places=2)
    car = models.DecimalField(max_digits=8, decimal_places=2)

class Expense(models.Model):
    # Date for user expenses
    # Defaults to today's date value
    date = models.DateField(default=date.today, blank=True)

    # Various user expense types
    food = models.OneToOneField(Food)
    housing = models.OneToOneField(Housing)
    utilities = models.OneToOneField(Utilities)
    transportation = models.OneToOneField(Transportation)
    insurance = models.OneToOneField(Insurance)
    clothes = models.DecimalField(max_digits=8, decimal_places=2)
    entertainment = models.DecimalField(max_digits=8, decimal_places=2)
    savings = models.DecimalField(max_digits=8, decimal_places=2)
    miscellaneous = models.DecimalField(max_digits=8, decimal_places=2)