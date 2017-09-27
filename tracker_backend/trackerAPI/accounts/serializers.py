from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        # TODO: Debug with password, delete in production
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'income', 'password', )

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(style={'input_type': 'username'}, required=True)
    password = serializers.CharField(style={'input_type': 'password'}, required=True)

    def validate(self, attrs):
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

class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(style={'input_type': 'username'}, required=True)
    email = serializers.CharField(style={'input_type': 'email'}, required=True)
    password = serializers.CharField(style={'input_type': 'password'}, required=True)

    def create(self, validated_data):
        user = UserSerializer.create(self, validated_data)
        user.set_password(validated_data['password'])

        user.save()

        return user

    class Meta:
        model = User
        # TODO: Debug with password, delete in production
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'income', 'password', )