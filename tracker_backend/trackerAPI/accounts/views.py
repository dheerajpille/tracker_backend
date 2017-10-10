from django.shortcuts import render
from django.core import serializers
from django.http import Http404, HttpResponse
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import *
import json

# Create your views here.
class LoginView(APIView):
    """
    Allows client to login with user credentials (username/password)
    """

    # Gives any user permission to POST for login
    permission_classes = {AllowAny, }

    def post(self, request):
        validate_user = LoginSerializer(data=request.data)

        if validate_user.is_valid():
            serializer = UserSerializer(validate_user.validated_data, context={'request': request})

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(validate_user.errors, status=status.HTTP_401_UNAUTHORIZED)


class SignupView(APIView):
    """
    Allows client to signup with user credentials (username/email/password)
    Other fields are optional
    """

    # Gives any user permission to POST for signup
    permission_classes = {AllowAny, }

    def post(self, request):
        create_user = SignupSerializer(data=request.data)

        if create_user.is_valid():
            create_user.save()
            serializer = UserSerializer(create_user.data, context={'request': request})

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(create_user.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    """
    Allows client to view, update, and delete their own data after authentication
    """

    # Obtains object in question via pk/id value
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    # View the User object
    def get(self, request, pk):
        user = self.get_object(pk)
        if request.user.is_superuser or request.user == user:
            serializer = UserSerializer(user, context={'request', request})
            return Response(serializer.data)
        else:
            return Response(data={"message": "Not authorized to view this user."}, status=status.HTTP_401_UNAUTHORIZED)

    # Update the User object
    def put(self, request, pk):
        user = self.get_object(pk)
        if request.user.is_superuser or request.user == user:
            serializer = UserSerializer(user, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()

                return Response(serializer.data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(data={"message": "Not authorized to edit this user."}, status=status.HTTP_401_UNAUTHORIZED)

    # Delete the User object
    def delete(self, pk):
        user = self.get_object(pk)

        if request.user.is_superuser or request.user == user:
            user.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(data={"message": "Not authorized to delete this user."}, status=status.HTTP_401_UNAUTHORIZED)


class UserList(ListAPIView):
    """
    Allows admin to view all users in database
    """

    # Disables pagination for GET calls
    pagination_class = None

    # Gives list-viewing access to superuser/admin accounts only
    permission_classes = {IsAdminUser, }

    serializer_class = UserSerializer

    # Orders queryset of user accounts by pk/id value
    queryset = User.objects.all().order_by('id')


# TODO: replace get_object with get_object_or_404?
# TODO: change this to Expense, since EI is too long for me
class CreateExpense(APIView):

    # TODO: remove this later, it was useful for the most frustrating problem
    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }


    def post(self, request, pk):

        create_expense = ExpenseSerializer(data=request.data, context={'request': request})

        if create_expense.is_valid():

            # Creates an Expense if it does not expect in database
            if not Expense.objects.filter(date__exact=self.request.data['date'],
                                          category__iexact=self.request.data['category'],
                                          type__iexact=self.request.data['type']).exists():

                create_expense.save()
                serializer = ExpenseSerializer(create_expense.data)

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:

                return Response(data={"message": "Expense already created."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(create_expense.errors, status=status.HTTP_400_BAD_REQUEST)


class ExpenseList(ListAPIView):
    """
    Allows user to view their own expense list
    """

    # Disables pagination for GET calls
    pagination_class = None

    serializer_class = ExpenseSerializer
    model = Expense

    # TODO: make an error for empty queryset
    def get_queryset(self):
        # Filters all expense objects that were created by the current user
        queryset = self.model.objects.filter(user=self.request.user).order_by('-date').order_by('category')\
            .order_by('type')

        # Sorts printed response by date chronologically and by category/type alphabetically
        return queryset

class ExpenseDateList(ListAPIView):
    pagination_class = None

    serializer_class = ExpenseSerializer
    model = Expense

    def get(self, request, pk, date):
        queryset = self.model.objects.filter(user=self.request.user, date=date)
        serializer = ExpenseSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ExpenseCategoryList(ListAPIView):
    pagination_class = None

    serializer_class = ExpenseSerializer
    model = Expense

    def get(self, request, pk, category):
        queryset = self.model.objects.filter(user=self.request.user, category__iexact=category)
        serializer = ExpenseSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
