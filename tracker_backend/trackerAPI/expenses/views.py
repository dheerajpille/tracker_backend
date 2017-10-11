from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response

from tracker_backend.trackerAPI.expenses.models import Expense
from django.contrib.auth.models import User
from tracker_backend.trackerAPI.expenses.serializers import ExpenseSerializer


class CreateExpenseView(APIView):

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def post(self, request, pk):
        user = self.get_object(pk)
        create_expense = ExpenseSerializer(data=request.data, context={'request': request})

        if create_expense.is_valid():

            # Creates Expense if not existing in database
            if not Expense.objects.filter(user=user, date__exact=self.request.data['date'],
                                          category__iexact=self.request.data['category'],
                                          type__iexact=self.request.data['type']).exists():

                create_expense.save()
                serializer = ExpenseSerializer(create_expense.data)

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:

                return Response(data={"error": "Expense already created."}, status=status.HTTP_400_BAD_REQUEST)
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

    def get_queryset(self):
        # Filters all expense objects that were created by the current user
        queryset = self.model.objects.filter(user=self.request.user).order_by('-date')

        # Checks if expenses exist for user, and returns error if none are found
        if not queryset.exists():
            return Response(data={"error": "No expense found."}, status=status.HTTP_404_NOT_FOUND)

        # Sorts printed response by date chronologically
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
