from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    """
    Standard serializer for standard User model
    """

    class Meta:
        # Specifies model
        model = User

        # Displays the following fields in User response body
        fields = ('id', 'username', 'first_name', 'last_name', 'email', )


class LoginSerializer(serializers.Serializer):
    """
    Login serializer, which validates client's username and password with database
    """

    # JSON fields rendered for input
    username = serializers.CharField(style={'input_type': 'username'}, required=True)
    password = serializers.CharField(style={'input_type': 'password'}, required=True)

    # Validates login credentials with database
    def validate(self, attrs):

        # Gets username and password fields from given data
        username = attrs.get('username')
        password = attrs.get('password')

        # Authenticates username and password with database
        user = authenticate(request=self.context.get('request'), username=username, password=password)

        # Checks if User was found, raises ValidationError otherwise
        if user:
            pass
        else:
            # ValidationError when username/password is incorrect and not matching with any User in database
            raise ValidationError('Unable to login with provided credentials.')

        # Gives User if found
        return user

    class Meta:
        # Specifies model
        model = User

        # Lists fields given to serializer
        fields = ('username', 'password', )

        # Declares password field to not be shown in response
        write_only_fields = ('password', )


class SignupSerializer(serializers.Serializer):
    """
    Signup serializer, which creates a new User account with required credentials
    """

    # JSON fields rendered for input/response body
    # Only username/email/password fields required, id is automatically created, rest are optional
    id = serializers.ReadOnlyField()
    username = serializers.CharField(style={'input_type': 'username'}, required=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.CharField(style={'input_type': 'email'}, required=True)
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True, required=True)

    # Creates new User in database with given data
    def create(self, validated_data):

        # TODO: add in email check and verification
        # Checks whether username already exists in database
        try:
            username = User.objects.get(username__iexact=self.validated_data['username'])

        except User.DoesNotExist:

            # Checks whether email already exists in database
            try:
                email = User.objects.get(email__iexact=self.validated_data['email'])

            except User.DoesNotExist:

                # Creates new User object through UserSerializer with given data
                user = UserSerializer.create(self, validated_data)

                # Sets user's password with password given on signup
                user.set_password(validated_data['password'])

                user.save()

                # Returns User details upon creation
                return user

            # Raised when email already exists in database
            raise ValidationError('A user with that email already exists.')

        # Raised when username already exists in database
        raise ValidationError('A user with that username already exists.')

    class Meta:

        # Specifies model
        model = User

        # List fields given to serializer
        fields = ('username', 'email', 'password', )

        # Declares password field to not be shown in response
        write_only_fields = ('password', )
