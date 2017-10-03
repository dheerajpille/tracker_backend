from django.contrib.auth import authenticate
from django.conf import settings
from django.utils.encoding import force_text
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, APIException

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

    class Meta:
        model = Food
        fields = ('groceries', 'restaurants', )


class HousingSerializer(serializers.ModelSerializer):
    """
    Standard serializer for housing model
    """

    class Meta:
        model = Housing
        fields = ('mortgage', 'rent', )


class UtilitiesSerializer(serializers.ModelSerializer):
    """
    Standard serializer for utilities model
    """

    class Meta:
        model = Utilities
        fields = ('hydro', 'electricity', 'gas', 'internet', 'mobile', 'television', )


class TransportationSerializer(serializers.ModelSerializer):
    """
    Standard serializer for transportation model
    """

    class Meta:
        model = Transportation
        fields = ('fuel', 'parking', 'public', )


class InsuranceSerializer(serializers.ModelSerializer):
    """
    Standard serializer for insurance model
    """

    class Meta:
        model = Insurance
        fields = ('health', 'household', 'car', )


class ClothesSerializer(serializers.ModelSerializer):
    """
    Standard serializer for clothes model
    """

    class Meta:
        model = Clothes
        fields = ('clothing', )


class EntertainmentSerializer(serializers.ModelSerializer):
    """
    Standard serializer for entertainment model
    """

    class Meta:
        model = Entertainment
        fields = ('electronics', 'games', 'movies', 'bar', )


class EducationSerializer(serializers.ModelSerializer):
    """
    Standard serializer for education model
    """

    class Meta:
        model = Education
        fields = ('tuition', ' textbooks', 'fees', )


class Miscellaneous(serializers.ModelSerializer):
    """
    Standard serializer for miscellaneous model
    """

    class Meta:
        model = Miscellaneous
        fields = ('other', )


class ExpenseSerializer(serializers.ModelSerializer):
    """
    Standard serializer for expense model
    """

    class Meta:
        model = Expense

        # Lists various expenses defined in expense model
        fields = ('food', 'housing', 'utilities', 'transportation', 'insurance', 'clothes', 'entertainment',
                  'education', 'savings', 'miscellaneous', )
