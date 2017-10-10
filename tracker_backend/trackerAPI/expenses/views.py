from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response

from tracker_backend.trackerAPI.expenses.models import Expense
from django.contrib.auth.models import User
from tracker_backend.trackerAPI.accounts.serializers import UserSerializer
from tracker_backend.trackerAPI.expenses.serializers import ExpenseSerializer
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from django.utils.timezone import now

# Create your views here.


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
        queryset = self.model.objects.filter(user=self.request.user, category__iexact=category).order_by('-date')
        serializer = ExpenseSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ExpenseTypeList(ListAPIView):
    pagination_class = None

    serializer_class = ExpenseSerializer
    model = Expense

    def get(self, request, pk, category, type):
        queryset = self.model.objects.filter(user=self.request.user, category__iexact=category, type__iexact=type)\
            .order_by('-date')
        serializer = ExpenseSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ExpenseDateCategoryList(ListAPIView):
    pagination_class = None

    serializer_class = ExpenseSerializer
    model = Expense

    def get(self, request, pk, date, category):
        queryset = self.model.objects.filter(user=self.request.user, date=date, category__iexact=category)\
            .order_by('-date')
        serializer = ExpenseSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ExpenseDateTypeList(ListAPIView):
    pagination_class = None

    serializer_class = ExpenseSerializer
    model = Expense

    def get(self, request, pk, date, category, type):
        expense = self.model.objects.filter(user=self.request.user, date=date, category__iexact=category,
                                            type__iexact=type).first()

        if expense is None:
            return Response(data={"message": "Expense not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ExpenseSerializer(expense)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, date, category, type):
        expense = self.model.objects.filter(user=self.request.user, date=date, category__iexact=category,
                                            type__iexact=type).first()
        if expense is None:
            return Response(data={"message": "Expense not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ExpenseSerializer(expense, data=request.data, partial=True, context={'request': request})

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, date, category, type):
        expense = self.model.objects.filter(user=self.request.user, date=date, category__iexact=category,
                                            type__iexact=type).first()
        if expense is None:
            return Response(data={"message": "Expense not found."}, status=status.HTTP_404_NOT_FOUND)

        expense.delete()

        return Response(data={"message": "Expense deleted."}, status=status.HTTP_204_NO_CONTENT)
