from django.shortcuts import render
from django.http import Http404
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response

from tracker_backend.trackerAPI.serializers import UserSerializer
from tracker_backend.trackerAPI.expenses.serializers import ExpenseSerializer
from tracker_backend.trackerAPI.expenses.models import Expense
from django.contrib.auth.models import User
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from django.utils.timezone import now


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


class WeeklyTotalReport(ListAPIView):
    pagination_class = None

    serializer_class = ExpenseSerializer
    model = Expense

    def get(self, request, pk):
        today = date.today()
        week_start = today - timedelta(days=today.isoweekday() % 7)

        queryset = self.model.objects.filter(user=self.request.user, date__range=(week_start, today))

        # Checks if queryset is not empty
        if queryset.exists():
            sum = 0
            for expense in queryset:
                sum += expense.value
            return Response(sum, status=status.HTTP_200_OK)
        else:
            return Response(data={"message": "No expenses found in the past year."}, status=status.HTTP_204_NO_CONTENT)