from django.contrib.auth.models import User
from django.http import Http404

from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from tracker_backend.trackerAPI.serializers import UserSerializer, LoginSerializer, SignupSerializer


class LoginView(APIView):
    """
    Logs client in with required User credentials (username/password)
    """

    # Gives any user permission to POST for login
    permission_classes = {AllowAny, }

    # POST data for login request
    def post(self, request):

        # Gets data from POST call and places it in LoginSerializer
        validate_user = LoginSerializer(data=request.data)

        # Checks if given data is valid
        if validate_user.is_valid():

            # Places the aforementioned data in UserSerializer
            serializer = UserSerializer(validate_user.validated_data, context={'request': request})

            # Logs User into API
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Returns any errors found in POST data
        return Response(validate_user.errors, status=status.HTTP_401_UNAUTHORIZED)


class SignupView(APIView):
    """
    Signs client up with required User credentials (username/email/password)
    Partial input of other User fields allowed
    """

    # Gives any user permission to POST for signup
    permission_classes = {AllowAny, }

    # POST data for signup request
    def post(self, request):

        # Gets data from POST call and places it in SignupSerializer
        create_user = SignupSerializer(data=request.data)

        # Checks if given data is valid
        if create_user.is_valid():

            create_user.save()

            # Places the aforementioned data in UserSerializer
            serializer = UserSerializer(create_user.data, context={'request': request})

            # Creates new User object in database
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Returns any errors found in POST data
        return Response(create_user.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    """
    Allows client to view, update, and delete their own User data after authentication
    """

    # Gets User object via pk/id value
    # Returns user or 404, if not found
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    # Gets the current User object
    def get(self, request, pk):

        # Finds current User in database
        user = self.get_object(pk)

        # Checks if the user sending the request is the user in question
        if request.user == user:

            # Serializes User data to UserSerializer
            serializer = UserSerializer(user, context={'request', request})

            # Returns User's data as response
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Returns when unauthorized access to User's data occurs
        return Response(data={"message": "Not authorized to view this user."}, status=status.HTTP_401_UNAUTHORIZED)

    # Updates the current User object
    # Partial input of User fields allowed
    def put(self, request, pk):

        # Finds current User in database
        user = self.get_object(pk)

        # Checks if the user sending the request is the user in question
        if request.user == user:

            # Serializes User data to UserSerializer
            serializer = UserSerializer(user, data=request.data, partial=True, context={'request': request})

            # Checks if given data from PUT call is valid
            if serializer.is_valid():

                serializer.save()

                # Saves the updated User information in database
                return Response(serializer.data, status=status.HTTP_200_OK)

            # Returns errors that occur with PUT call data
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Returns when unauthorized access to User's data occurs
        return Response(data={"message": "Not authorized to edit this user."}, status=status.HTTP_401_UNAUTHORIZED)

    # Delete the User object
    def delete(self, pk):

        # Finds current User in database
        user = self.get_object(pk)

        # Checks if the user sending the request is the user in question
        if request.user == user:

            # Deletes User object from database
            user.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        # Returns when unauthorized access to User's data occurss
        return Response(data={"message": "Not authorized to delete this user."}, status=status.HTTP_401_UNAUTHORIZED)


class UserList(ListAPIView):
    """
    Allows superuser/admin to view all Users in database
    """

    # Disables pagination for GET calls
    pagination_class = None

    # Gives User list access to superuser/admin accounts only
    permission_classes = {IsAdminUser, }

    # Specifies serializer class
    serializer_class = UserSerializer

    # Orders queryset of user accounts by pk/id value
    queryset = User.objects.all().order_by('id')
