from rest_framework import serializers

from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Standard serializer for custom user model
    """

    class Meta:
        model = User

        # Displays the following fields as response body
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'budget', )