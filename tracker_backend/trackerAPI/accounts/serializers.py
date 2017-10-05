import json, simplejson

from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import *


class UserSerializer(serializers.ModelSerializer):
    """
    Standard serializer for custom user model
    """

    class Meta:
        model = User

        # Displays the following fields as response body
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'budget', )


class LoginSerializer(serializers.Serializer):
    """
    Login serializer, which validates client's username and password with database
    """

    # JSON fields rendered for input
    username = serializers.CharField(style={'input_type': 'username'}, required=True)
    password = serializers.CharField(style={'input_type': 'password'}, required=True)

    def validate(self, attrs):
        """
        Validates user credentials with database
        :param attrs: user credentials passed from API call
        :return: User object if existing, error if not
        """
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(request=self.context.get('request'), username=username, password=password)

        if user:
            pass
        else:
            raise ValidationError('Unable to login with provided credentials.')

        return user

    class Meta:
        model = User
        fields = ('username', 'password', )
        write_only_fields = ('password', )


class SignupSerializer(serializers.Serializer):
    """
    Signup serializer, which creates a new user account with required/proper credentials
    """

    # JSON fields rendered for input/response body
    id = serializers.ReadOnlyField()
    username = serializers.CharField(style={'input_type': 'username'}, required=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.CharField(style={'input_type': 'email'}, required=True)
    budget = serializers.DecimalField(max_digits=8, decimal_places=2, required=False)
    currency = serializers.CharField(required=False)
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True, required=True)

    def create(self, validated_data):
        """
        Creates a new user account in database with given credentials
        :param validated_data: Inputted user credentials, passed from API call
        :return: Created user object if successful, error(s) if not
        """

        # TODO: add in email check and verification
        # Checks whether the username already exists in database
        try:
            username = User.objects.get(username__iexact=self.validated_data['username'])
        except User.DoesNotExist:

            # Checks whether the email already exists in database
            try:
                email = User.objects.get(email__iexact=self.validated_data['email'])
            except User.DoesNotExist:
                user = UserSerializer.create(self, validated_data)
                user.set_password(validated_data['password'])

                user.save()

                return user

            raise ValidationError('A user with that email already exists.')

        # TODO: change to display multiple errors if triggered
        # TODO: add custom message preface, similar to user detail message

        raise ValidationError('A user with that username already exists.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password', )
        write_only_fields = ('password', )


class FoodSerializer(serializers.ModelSerializer):
    """
    Standard serializer for food model
    """
    groceries = serializers.DecimalField(max_digits=8, decimal_places=2, default=0, required=False)
    restaurants = serializers.DecimalField(max_digits=8, decimal_places=2, default=0, required=False)

    class Meta:
        model = Food
        fields = ('groceries', 'restaurants', )


class HousingSerializer(serializers.ModelSerializer):
    """
    Standard serializer for housing model
    """
    mortgage = serializers.DecimalField(max_digits=8, decimal_places=2, default=0, required=False)
    rent = serializers.DecimalField(max_digits=8, decimal_places=2, default=0, required=False)

    class Meta:
        model = Housing
        fields = ('mortgage', 'rent', )


class UtilitiesSerializer(serializers.ModelSerializer):
    """
    Standard serializer for utilities model
    """
    hydro = serializers.DecimalField(max_digits=8, decimal_places=2, default=0, required=False)
    electricity = serializers.DecimalField(max_digits=8, decimal_places=2, default=0, required=False)
    gas = serializers.DecimalField(max_digits=8, decimal_places=2, default=0, required=False)
    internet = serializers.DecimalField(max_digits=8, decimal_places=2, default=0, required=False)
    mobile = serializers.DecimalField(max_digits=8, decimal_places=2, default=0, required=False)
    television = serializers.DecimalField(max_digits=8, decimal_places=2, default=0, required=False)

    class Meta:
        model = Utilities
        fields = ('hydro', 'electricity', 'gas', 'internet', 'mobile', 'television', )


class TransportationSerializer(serializers.ModelSerializer):
    """
    Standard serializer for transportation model
    """
    fuel = serializers.DecimalField(max_digits=8, decimal_places=2, default=0, required=False)
    parking = serializers.DecimalField(max_digits=8, decimal_places=2, default=0, required=False)
    public = serializers.DecimalField(max_digits=8, decimal_places=2, default=0, required=False)

    class Meta:
        model = Transportation
        fields = ('fuel', 'parking', 'public', )


class InsuranceSerializer(serializers.ModelSerializer):
    """
    Standard serializer for insurance model
    """
    health = serializers.DecimalField(max_digits=8, decimal_places=2, default=0, required=False)
    household = serializers.DecimalField(max_digits=8, decimal_places=2, default=0, required=False)
    car = serializers.DecimalField(max_digits=8, decimal_places=2, default=0, required=False)

    class Meta:
        model = Insurance
        fields = ('health', 'household', 'car', )


class ClothesSerializer(serializers.ModelSerializer):
    """
    Standard serializer for clothes model
    """
    clothing = serializers.DecimalField(max_digits=8, decimal_places=2, default=0, required=False)

    class Meta:
        model = Clothes
        fields = ('clothing', )


class EntertainmentSerializer(serializers.ModelSerializer):
    """
    Standard serializer for entertainment model
    """
    electronics = serializers.DecimalField(max_digits=8, decimal_places=2, default=0, required=False)
    games = serializers.DecimalField(max_digits=8, decimal_places=2, default=0, required=False)
    movies = serializers.DecimalField(max_digits=8, decimal_places=2, default=0, required=False)
    bar = serializers.DecimalField(max_digits=8, decimal_places=2, default=0, required=False)

    class Meta:
        model = Entertainment
        fields = ('electronics', 'games', 'movies', 'bar', )


class EducationSerializer(serializers.ModelSerializer):
    """
    Standard serializer for education model
    """
    tuition = serializers.DecimalField(max_digits=8, decimal_places=2, default=0, required=False)
    textbooks = serializers.DecimalField(max_digits=8, decimal_places=2, default=0, required=False)
    fees = serializers.DecimalField(max_digits=8, decimal_places=2, default=0, required=False)

    class Meta:
        model = Education
        fields = ('tuition', 'textbooks', 'fees', )


class SavingsSerializer(serializers.ModelSerializer):
    """
    Standard serializer for savings model
    """
    deposit = serializers.DecimalField(max_digits=8, decimal_places=2, default=0, required=False)

    class Meta:
        model = Savings
        fields = ('deposit', )


class MiscellaneousSerializer(serializers.ModelSerializer):
    """
    Standard serializer for miscellaneous model
    """
    other = serializers.DecimalField(max_digits=8, decimal_places=2, default=0, required=False)

    class Meta:
        model = Miscellaneous
        fields = ('other', )


class ExpenseSerializer(serializers.ModelSerializer):
    """
    Standard serializer for expense model
    """
    date = serializers.CharField(max_length=10, required=False)

    food = FoodSerializer()
    housing = HousingSerializer()
    utilities = UtilitiesSerializer()
    transportation = TransportationSerializer()
    insurance = InsuranceSerializer()
    clothes = ClothesSerializer()
    entertainment = EntertainmentSerializer()
    education = EducationSerializer()
    savings = SavingsSerializer()
    miscellaneous = MiscellaneousSerializer()

    def create(self, validated_data):
        date = self.validated_data['date']

        food_data = self.validated_data['food']
        food = Food.objects.create(**food_data)

        housing_data = validated_data['housing']
        housing = Housing.objects.create(**housing_data)

        utilities_data = validated_data['utilities']
        utilities = Utilities.objects.create(**utilities_data)

        transportation_data = validated_data['transportation']
        transportation = Transportation.objects.create(**transportation_data)

        insurance_data = validated_data['insurance']
        insurance = Insurance.objects.create(**insurance_data)

        clothes_data = validated_data['clothes']
        clothes = Clothes.objects.create(**clothes_data)

        entertainment_data = validated_data['entertainment']
        entertainment = Entertainment.objects.create(**entertainment_data)

        education_data = validated_data['education']
        education = Education.objects.create(**education_data)

        savings_data = validated_data['savings']
        savings = Savings.objects.create(**savings_data)

        miscellaneous_data = validated_data['miscellaneous']
        miscellaneous = Miscellaneous.objects.create(**miscellaneous_data)

        expense = Expense.objects.create(date=date, food=food, housing=housing, utilities=utilities,
                                         transportation=transportation, insurance=insurance, clothes=clothes,
                                         entertainment=entertainment, education=education, savings=savings,
                                         miscellaneous=miscellaneous)

        expense.save()

        return expense

    class Meta:
        model = Expense

        # Lists various expenses defined in expense model
        fields = ('date', 'food', 'housing', 'utilities', 'transportation', 'insurance', 'clothes',
                  'entertainment', 'education', 'savings', 'miscellaneous', )


class ExpenseItemSerializer(serializers.ModelSerializer):
    date = serializers.DateField(required=True)

    user = UserSerializer()

    category = serializers.CharField(max_length=32, required=True)
    type = serializers.CharField(max_length=32, required=True)
    value = serializers.DecimalField(max_digits=8, decimal_places=2, required=True)
    currency = serializers.CharField(max_length=3, required=True)

    class Meta:
        model = ExpenseItem

        fields = ('date', 'user', 'category', 'type', 'value', 'currency', )
