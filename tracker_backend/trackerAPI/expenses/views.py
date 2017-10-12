from datetime import date, timedelta

from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from tracker_backend.trackerAPI.expenses.models import Expense
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

                # Returns created expense data as JSON response
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
        queryset = Expense.objects.filter(user=self.request.user).order_by('-date')

        # Checks if any expenses exist for current User
        if not queryset.exists():

            # TODO: fix this, returns "response content must be rendered before it can be iterated over"
            # Returns error if no expenses are found for current User in database
            return Response(data={"error": "No types found."}, status=status.HTTP_404_NOT_FOUND)

        # Returns queryset of all Expense objects found for current User
        return queryset


class ExpenseDateList(ListAPIView):
    """
    Gets User's Expense list on a specified date
    """

    # Disables pagination for GET call
    pagination_class = None

    # Specifies serializer and model types
    serializer_class = ExpenseSerializer
    model = Expense

    # Gets all Expense objects for a specified date
    def get(self, request, pk, date):

        # Filters all Expense objects that were created by current User with the specified date
        queryset = Expense.objects.filter(user=self.request.user, date=date)

        # Checks if any expenses exist on this date for current User
        if not queryset.exists():

            # Returns error if no expenses are found on this date for current User in database
            return Response(data={"error": "No expenses found."}, status=status.HTTP_404_NOT_FOUND)

        # Serializes queryset data into ExpenseSerializer, where multiple Expenses are allowed/expected
        serializer = ExpenseSerializer(queryset, many=True)

        # Returns specified list of expenses
        return Response(serializer.data, status=status.HTTP_200_OK)


class ExpenseCategoryList(ListAPIView):
    """
    Gets User's expense list for a certain category
    """

    # Disables pagination for GET call
    pagination_class = None

    # Specifies serializer and model types
    serializer_class = ExpenseSerializer
    model = Expense

    # Gets all Expense objects for a certain category
    def get(self, request, pk, category):

        # Filters all Expense objects that were created by current User in a certain category
        # Converts slugs in category URL to spaces for filtering purposes
        queryset = Expense.objects.filter(user=self.request.user, category__iexact=category.replace('-', ' '))\
            .order_by('-date')

        # Checks if any expenses exist in this category for current User
        if not queryset.exists():

            # Returns error if no expenses are found in this category for current User in database
            return Response(data={"error": "No expenses found."}, status=status.HTTP_404_NOT_FOUND)

        # Serializes queryset data into Expense serializer, where multiple Expenses are allowed/expected
        serializer = ExpenseSerializer(queryset, many=True)

        # Returns specified list of expenses
        return Response(serializer.data, status=status.HTTP_200_OK)


class ExpenseTypeList(ListAPIView):
    """
    Gets User's expense list for a certain type in a certain category
    """

    # Disables pagination for GET call
    pagination_class = None

    # Specifies serializer and model types
    serializer_class = ExpenseSerializer
    model = Expense

    # Gets all Expense objects for a cetain type in a certain category
    def get(self, request, pk, category, type):

        # Filters all Expense objects that were created by current User in a certain type in a certain category
        # Converts slugs in category URL to spaces for filtering purposes
        queryset = Expense.objects.filter(user=self.request.user, category__iexact=category.replace('-', ' '),
                                             type__iexact=type.replace('-', ' ')).order_by('-date')

        # Checks if any expenses exist in this category for current User
        if not queryset.exists():

            # Returns error if no expenses are found in this category for current User in database
            return Response(data={"error": "No expenses found."}, status=status.HTTP_404_NOT_FOUND)

        # Serializes queryset data into Expense serializer, where multiple Expenses are allowed/expected
        serializer = ExpenseSerializer(queryset, many=True)

        # Returns specified list of expenses
        return Response(serializer.data, status=status.HTTP_200_OK)


class ExpenseDateCategoryList(ListAPIView):
    """
    Gets User's expense list for a certain category on a specified date
    """

    # Disables pagination for GET call
    pagination_class = None

    # Specifies serializer and model types
    serializer_class = ExpenseSerializer
    model = Expense

    # Gets all Expense objects for a certain category on a specified date
    def get(self, request, pk, date, category):

        # Filters all Expense objects that were created by current User in a certain category on a specified date
        # Converts slugs in category URL to spaces for filtering purposes
        queryset = Expense.objects.filter(user=self.request.user, date=date,
                                          category__iexact=category.replace('-', ' ')).order_by('-date')

        # Checks if any expenses exist in this category for current User
        if not queryset.exists():

            # Returns error if no expenses are found in this category for current User in database
            return Response(data={"error": "No expenses found."}, status=status.HTTP_404_NOT_FOUND)

        # Serializes queryset data into Expense serializer, where multiple Expenses are allowed/expected
        serializer = ExpenseSerializer(queryset, many=True)

        # Returns specified list of expenses
        return Response(serializer.data, status=status.HTTP_200_OK)


class ExpenseDetail(APIView):

    # Gets the specific Expense object defined by date, category, and type
    def get(self, request, pk, date, category, type):

        # Filters the Expense object with date, category, and type to get the object in question
        # Converts slugs in category URL to spaces for filtering purposes
        expense = Expense.objects.filter(user=self.request.user, date=date, category__iexact=category.replace('-', ' '),
                                         type__iexact=type.replace('-', ' ')).first()

        # Checks if expense exists
        if expense is None:

            # Returns error if expense is not found
            return Response(data={"error": "Expense not found."}, status=status.HTTP_404_NOT_FOUND)

        # Serializes expense into ExpenseSerializer
        serializer = ExpenseSerializer(expense)

        # Returns specified expense
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Updates the specific Expense object defined by date, category, and type
    def put(self, request, pk, date, category, type):

        # Filters the Expense object with date, category, and type to get the object in question
        # Converts slugs in category URL to spaces for filtering purposes
        expense = Expense.objects.filter(user=self.request.user, date=date, category__iexact=category.replace('-', ' '),
                                         type__iexact=type.replace('-', ' ')).first()

        # Checks if expense exists
        if expense is None:

            # Returns error if expense is not found
            return Response(data={"error": "Expense not found."}, status=status.HTTP_404_NOT_FOUND)

        # Serializes expense into ExpenseSerializer
        serializer = ExpenseSerializer(expense, data=request.data, partial=True, context={'request': request})

        # Checks if serializer is valid
        if serializer.is_valid():

            serializer.save()

            # Returns updated specified expense
            return Response(serializer.data)

        # Returns errors that occur when attempting to update Expense
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Deletes the specific Expense object defined by date, category, and type
    def delete(self, request, pk, date, category, type):

        # Filters the Expense object with date, category, and type to get the object in question
        # Converts slugs in category URL to spaces for filtering purposes
        expense = Expense.objects.filter(user=self.request.user, date=date, category__iexact=category.replace('-', ' '),
                                         type__iexact=type.replace('-', ' ')).first()

        # Checks if expense exists
        if expense is None:

            # Returns error if expense is not f ound
            return Response(data={"error": "Expense not found."}, status=status.HTTP_404_NOT_FOUND)

        # Deletes Expense object if found
        expense.delete()

        # Returns a statement displaying that expense has been successfully deleted
        return Response(data={"message": "Expense deleted."}, status=status.HTTP_204_NO_CONTENT)


class DateList(ListAPIView):
    """
    Gets User's distinct dates for expenses
    """

    # Gets distinct dates for current User
    def get(self, request, pk):

        # Initializes an empty list for distinct dates
        date_list = []

        # Filters queryset for distinct dates in reverse chronological order
        queryset = Expense.objects.order_by('-date').values('date').distinct()

        # Checks if queryset is not empty
        if not queryset.exists():

            # Returns error if no dates are found (no expenses created)
            return Response(data={"error": "No dates found."}, status=status.HTTP_404_NOT_FOUND)

        # Iterates through distinct dates in queryset
        for q in queryset:

            # Appends distinct date values to date_list
            date_list.append(q['date'])

        # Returns list of distinct dates
        return Response(date_list, status=status.HTTP_200_OK)


class CategoryList(ListAPIView):
    """
    Gets User's distinct categories for expenses
    """

    # Gets distinct categories for current User
    def get(self, request, pk):

        # Initializes an empty list for distinct categories
        category_list = []

        # Filters queryset for distinct dates in alphabetical order
        queryset = Expense.objects.order_by('category').values('category').distinct()

        # Checks if queryset is not empty
        if not queryset.exists():

            # Returns error if no categories are found (no expenses created)
            return Response(data={"error": "No categories found."}, status=status.HTTP_404_NOT_FOUND)

        # Iterates through distinct categories in queryset
        for q in queryset:

            # Appends distinct category values to category_list
            category_list.append(q['category'])

        # Returns list of distinct categories
        return Response(category_list, status=status.HTTP_200_OK)


class TypeList(ListAPIView):
    """
    Gets User's distinct types from a certain category for expenses
    """

    # Gets distinct types of a certain category for current User
    def get(self, request, pk, category):

        # Initializes an empty list for distinct types in a certain category
        type_list = []

        # Filters queryset for distinct types in a certain category in alphabetical order

        queryset = Expense.objects.filter(user=self.request.user, category__iexact=category.replace('-', ' '))\
            .order_by('type').values('type').distinct()

        # Checks if queryset is not empty
        if not queryset.exists():

            # Returns error if no categories are found (no expenses created)
            return Response(data={"error": "No types found."}, status=status.HTTP_404_NOT_FOUND)

        # Iterates through distinct types in certain category in queryset
        for q in queryset:

            # Appends distinct type values to type_list
            type_list.append(q['type'])

        # Returns list of distinct types from a certain category
        return Response(type_list, status=status.HTTP_200_OK)


class WeeklyExpenseList(ListAPIView):
    """
    Gets User's list of expenses for current week
    """

    # Disables pagination for GET calls
    pagination_class = None

    # Specifies serializer and model types
    serializer_class = ExpenseSerializer
    model = Expense

    # Gets list of expenses made in current week
    def get(self, request, pk):
        
        # Determines the today's and the week's start (Sunday of current week) ISO-8601 values
        today = date.today()
        week_start = today - timedelta(days=today.isoweekday() % 7)
            
        # Queryset of expenses within specified date range
        queryset = Expense.objects.filter(user=self.request.user, date__range=(week_start, today))

        # Checks if queryset is not empty
        if not queryset.exists():

            # Returns error if no expenses are found in current week for current User in database
            return Response(data={"error": "No expenses found in current week."}, status=status.HTTP_404_NOT_FOUND)

        # Serializes queryset data into Expense serializer, where multiple Expenses are allowed/expected
        serializer = ExpenseSerializer(queryset, many=True)

        # Returns list of expenses in current week
        return Response(serializer.data, status=status.HTTP_200_OK)


class MonthlyExpenseList(ListAPIView):
    """
    Gets User's list of expenses for current month
    """

    # Disables pagination for GET calls
    pagination_class = None

    # Specifies serializer and model types
    serializer_class = ExpenseSerializer
    model = Expense

    # Gets list of expenses made in current month
    def get(self, request, pk):

        # Determines the today's and the month's start (1st of current month) ISO-8601 values
        today = date.today()
        month_start = today.replace(day=1)

        # Queryset of expenses within specified date range
        queryset = Expense.objects.filter(user=self.request.user, date__range=[month_start, today])

        # Checks if queryset is not empty
        if not queryset.exists():
            # Returns error if no expenses are found in current month for current User in database
            return Response(data={"error": "No expenses found in current month."}, status=status.HTTP_404_NOT_FOUND)

        # Serializes queryset data into Expense serializer, where multiple Expenses are allowed/expected
        serializer = ExpenseSerializer(queryset, many=True)

        # Returns list of expenses in current month
        return Response(serializer.data, status=status.HTTP_200_OK)


class YearlyExpenseList(ListAPIView):
    """
    Gets User's list of expenses for current year
    """

    # Disables pagination for GET calls
    pagination_class = None

    # Specifies serializer and model types
    serializer_class = ExpenseSerializer
    model = Expense

    # Gets list of expenses made in current year
    def get(self, request, pk):

        # Determines the today's and the year's start (1st of current year) ISO-8601 values
        today = date.today()
        year_start = today.replace(month=1, day=1)

        # Queryset of expenses within specified date range
        queryset = Expense.objects.filter(user=self.request.user, date__range=[year_start, today])

        # Checks if queryset is not empty
        if not queryset.exists():

            # Returns error if no expenses are found in current year for current User in database
            return Response(data={"error": "No expenses found in current year."}, status=status.HTTP_404_NOT_FOUND)

        # Serializes queryset data into Expense serializer, where multiple Expenses are allowed/expected
        serializer = ExpenseSerializer(queryset, many=True)

        # Returns list of expenses in current year
        return Response(serializer.data, status=status.HTTP_200_OK)
