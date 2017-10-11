from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from tracker_backend.trackerAPI.expenses.serializers import ExpenseSerializer
from tracker_backend.trackerAPI.expenses.models import Expense
from datetime import date, timedelta


class WeeklyExpenseReport(ListAPIView):
    pagination_class = None

    serializer_class = ExpenseSerializer
    model = Expense

    def get(self, request, pk):
        today = date.today()
        week_start = today - timedelta(days=today.isoweekday() % 7)

        queryset = self.model.objects.filter(user=self.request.user, date__range=(week_start, today))

        # Checks if queryset is not empty
        if queryset.exists():
            serializer = ExpenseSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data={"message": "No expenses found in the past week."}, status=status.HTTP_204_NO_CONTENT)


class MonthlyExpenseReport(ListAPIView):
    pagination_class = None

    serializer_class = ExpenseSerializer
    model = Expense

    def get(self, request, pk):
        today = date.today()
        month_start = today.replace(day=1)

        # Checks if queryset is not empty
        queryset = self.model.objects.filter(user=self.request.user, date__range=[month_start, today])

        if queryset.exists():
            serializer = ExpenseSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data={"message": "No expenses found in the past month."}, status=status.HTTP_204_NO_CONTENT)


class YearlyExpenseReport(ListAPIView):
    pagination_class = None

    serializer_class = ExpenseSerializer
    model = Expense

    def get(self, request, pk):
        today = date.today()
        year_start = today.replace(month=1, day=1)

        # Checks if queryset is not empty
        queryset = self.model.objects.filter(user=self.request.user, date__range=[year_start, today])

        if queryset.exists():
            serializer = ExpenseSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data={"message": "No expenses found in the past year."}, status=status.HTTP_204_NO_CONTENT)
