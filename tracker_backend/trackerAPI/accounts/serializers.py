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


class ExpenseItemSerializer(serializers.ModelSerializer):
    date = serializers.DateField(required=True)

    user = UserSerializer(required=False)

    category = serializers.CharField(max_length=32, required=True)
    type = serializers.CharField(max_length=32, required=True)
    value = serializers.DecimalField(max_digits=8, decimal_places=2, required=True)
    currency = serializers.CharField(max_length=3, required=False)

    def create(self, validated_data):

        date = self.validated_data['date']

        user = self.context['request'].user

        category = self.validated_data['category']
        type = self.validated_data['type']
        value = self.validated_data['value']
        currency = self.validated_data['currency']

        expenseItem = ExpenseItem.objects.create(date=date, user=user, category=category, type=type, value=value,
                                                 currency=currency, )
        expenseItem.save()

        return expenseItem

    class Meta:
        model = ExpenseItem
        fields = ('date', 'user', 'category', 'type', 'value', 'currency', )
        depth = 1
