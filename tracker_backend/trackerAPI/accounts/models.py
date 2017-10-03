from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date


# Create your models here.
class User(AbstractUser):
    """
    Custom user model with additional (monthly) budget and currency parameter
    """

    budget = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=3)


# Expense models hereon
class Food(models.Model):
    """
    Food model, containing restaurant and groceries expense data
    """
    groceries = models.DecimalField(max_digits=8, decimal_places=2)
    restaurants = models.DecimalField(max_digits=8, decimal_places=2)


class Housing(models.Model):
    """
    Housing model, containing housing and rent expense data
    """
    mortgage = models.DecimalField(max_digits=8, decimal_places=2)
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


class Clothes(models.Model):
    """
    Clothes model, containing clothing expense data
    """
    clothing = models.DecimalField(max_digits=8, decimal_places=2)


class Entertainment(models.Model):
    """
    Entertainment model, containing electronics, games, movies, and bar expense data
    """
    electronics = models.DecimalField(max_digits=8, decimal_places=2)
    games = models.DecimalField(max_digits=8, decimal_places=2)
    movies = models.DecimalField(max_digits=8, decimal_places=2)
    bar = models.DecimalField(max_digits=8, decimal_places=2)


class Education(models.Model):
    """
    Education model, containing tuition, textbooks, and fees expense data
    """
    tuition = models.DecimalField(max_digits=8, decimal_places=2)
    textbooks = models.DecimalField(max_digits=8, decimal_places=2)
    fees = models.DecimalField(max_digits=8, decimal_places=2)


class Savings(models.Model):
    """
    Savings model, containing deposit expense data
    """
    deposit = models.DecimalField(max_digits=8, decimal_places=2)


class Miscellaneous(models.Model):
    """
    Miscellaneous model, containing other expense data
    """
    other = models.DecimalField(max_digits=8, decimal_places=2)


class Expense(models.Model):
    """
    Expense model, which tracks all defined types of user expenses
    """

    # Date for user expenses in ISO 8601 format
    # Defaults to server's date value today
    date = models.DateField(default=date.today, blank=True)

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
