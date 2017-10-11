from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response

from tracker_backend.trackerAPI.expenses.models import Expense
from django.contrib.auth.models import User
from tracker_backend.trackerAPI.expenses.serializers import ExpenseSerializer


class CreateExpenseView(APIView):
    """
    Creates new Expense object for current User
    """

    # Gets User object by pk/id value
    # Returns user or 404, if not found
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    # Creates new Expense object
    def post(self, request, pk):

        # Gets current User
        user = self.get_object(pk)

        # Gets data from POST request
        create_expense = ExpenseSerializer(data=request.data, context={'request': request})

        # Checks if data is valid
        if create_expense.is_valid():
            # Creates Expense object if it does not exist in database for current User
            if not Expense.objects.filter(user=user, date__exact=self.request.data['date'],
                                          category__iexact=self.request.data['category'],
                                          type__iexact=self.request.data['type']).exists():
                create_expense.save()

                # Serializes data to ExpenseSerializer for JSON response
                serializer = ExpenseSerializer(create_expense.data)

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                # Returns error upon attempting to create an expense that has already been found in database
                return Response(data={"error": "Expense already created."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Lists various errors found with POST data
            return Response(create_expense.errors, status=status.HTTP_400_BAD_REQUEST)


class ExpenseList(ListAPIView):
    """
    Gets User their all-time Expense list
    """

    # Disables pagination for GET call
    pagination_class = None

    # Specifies serializer and model types
    serializer_class = ExpenseSerializer
    model = Expense

    # Gets queryset of all of current User's expenses
    def get_queryset(self):

        # Filters all Expense objects created by current User, sorted in reverse chronological order
        queryset = self.model.objects.filter(user=self.request.user).order_by('-date')

        # Checks if any expenses exist for current User
        if not queryset.exists():
            # Returns error if no expenses are found for current User in database
            return Response(data={"error": "No expenses found."}, status=status.HTTP_404_NOT_FOUND)

        # Returns queryset of all Expense objects found for current User
        return queryset


class ExpenseDateList(ListAPIView):
    """
    Gets User their Expense list on a specified date
    """

    # Disables pagination for GET call
    pagination_class = None

    # Specifies serializer and model types
    serializer_class = ExpenseSerializer
    model = Expense

    # Gets all Expense objects for a specified date
    def get(self, request, pk, date):

        # Filters all Expense objects that were created by current User with the specified date
        queryset = self.model.objects.filter(user=self.request.user, date=date)

        if not queryset.exists():
            return Response(data={"error": "No expenses found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ExpenseSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ExpenseCategoryList(ListAPIView):
    pagination_class = None

    serializer_class = ExpenseSerializer
    model = Expense

    def get(self, request, pk, category):
        queryset = self.model.objects.filter(user=self.request.user, category__iexact=category.replace('-', ' '))\
            .order_by('-date')
        serializer = ExpenseSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ExpenseTypeList(ListAPIView):
    pagination_class = None

    serializer_class = ExpenseSerializer
    model = Expense

    def get(self, request, pk, category, type):
        queryset = self.model.objects.filter(user=self.request.user, category__iexact=category.replace('-', ' '),
                                             type__iexact=type.replace('-', ' ')).order_by('-date')
        serializer = ExpenseSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ExpenseDateCategoryList(ListAPIView):
    pagination_class = None

    serializer_class = ExpenseSerializer
    model = Expense

    def get(self, request, pk, date, category):
        queryset = Expense.objects.filter(user=self.request.user, date=date,
                                          category__iexact=category.replace('-', ' ')).order_by('-date')
        serializer = ExpenseSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ExpenseDetail(APIView):
    def get(self, request, pk, date, category, type):
        expense = Expense.objects.filter(user=self.request.user, date=date, category__iexact=category.replace('-', ' '),
                                         type__iexact=type.replace('-', ' ')).first()

        if expense is None:
            return Response(data={"error": "Expense not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ExpenseSerializer(expense)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, date, category, type):
        expense = Expense.objects.filter(user=self.request.user, date=date, category__iexact=category.replace('-', ' '),
                                         type__iexact=type.replace('-', ' ')).first()
        if expense is None:
            return Response(data={"error": "Expense not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ExpenseSerializer(expense, data=request.data, partial=True, context={'request': request})

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, date, category, type):
        expense = Expense.objects.filter(user=self.request.user, date=date, category__iexact=category.replace('-', ' '),
                                         type__iexact=type.replace('-', ' ')).first()

        if expense is None:
            return Response(data={"error": "Expense not found."}, status=status.HTTP_404_NOT_FOUND)

        expense.delete()

        return Response(data={"message": "Expense deleted."}, status=status.HTTP_204_NO_CONTENT)
