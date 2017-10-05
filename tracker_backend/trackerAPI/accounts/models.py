from django.db import models
from django.contrib.auth.models import AbstractUser

from datetime import date
from django.utils import timezone


# Create your models here.
class User(AbstractUser):
    """
    Custom user model with additional (monthly) budget and currency parameter
    """
    budget = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)


# Expense models hereon
class Food(models.Model):
    """
    Food model, containing restaurant and groceries expense data
    """
    groceries = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    restaurants = models.DecimalField(max_digits=8, decimal_places=2, default=0)


class Housing(models.Model):
    """
    Housing model, containing housing and rent expense data
    """
    mortgage = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    rent = models.DecimalField(max_digits=8, decimal_places=2, default=0)


class Utilities(models.Model):
    """
    Utilities model, containing hydro, electricity, gas, internet, mobile, and television expense data
    """
    hydro = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    electricity = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    gas = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    internet = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    mobile = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    television = models.DecimalField(max_digits=8, decimal_places=2, default=0)


class Transportation(models.Model):
    """
    Transportation model, containing fuel, parking, and public expense data
    """
    fuel = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    parking = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    public = models.DecimalField(max_digits=8, decimal_places=2, default=0)


class Insurance(models.Model):
    """
    Insurance model, containing health, household, and car expense data
    """
    health = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    household = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    car = models.DecimalField(max_digits=8, decimal_places=2, default=0)


class Clothes(models.Model):
    """
    Clothes model, containing clothing expense data
    """
    clothing = models.DecimalField(max_digits=8, decimal_places=2, default=0)


class Entertainment(models.Model):
    """
    Entertainment model, containing electronics, games, movies, and bar expense data
    """
    electronics = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    games = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    movies = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    bar = models.DecimalField(max_digits=8, decimal_places=2, default=0)


class Education(models.Model):
    """
    Education model, containing tuition, textbooks, and fees expense data
    """
    tuition = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    textbooks = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    fees = models.DecimalField(max_digits=8, decimal_places=2, default=0)


class Savings(models.Model):
    """
    Savings model, containing deposit expense data
    """
    deposit = models.DecimalField(max_digits=8, decimal_places=2, default=0)


class Miscellaneous(models.Model):
    """
    Miscellaneous model, containing other expense data
    """
    other = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)


class Expense(models.Model):
    """
    Expense model, which tracks all defined types of user expenses
    """

    # Date for user expenses in ISO 8601 format
    date = models.CharField(max_length=10)

    # User object that expense is connected to
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    # Various user expense types
    food = models.OneToOneField(Food)
    housing = models.OneToOneField(Housing)
    utilities = models.OneToOneField(Utilities)
    transportation = models.OneToOneField(Transportation)
    insurance = models.OneToOneField(Insurance)
    clothes = models.OneToOneField(Clothes)
    entertainment = models.OneToOneField(Entertainment)
    education = models.OneToOneField(Education)
    savings = models.OneToOneField(Savings)
    miscellaneous = models.OneToOneField(Miscellaneous)


class ExpenseItem(models.Model):
    date = models.DateField(blank=False, null=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    category = models.CharField(max_length=32, blank=False, null=False)
    type = models.CharField(max_length=32, blank=False, null=False)
    value = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, blank=False, null=False, default='CAD')