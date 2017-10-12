import json, simplejson

from datetime import date, timedelta

from django.db.models import Sum

from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from tracker_backend.trackerAPI.expenses.models import Expense
from tracker_backend.trackerAPI.expenses.serializers import ExpenseSerializer


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


class WeeklyTotal(APIView):

    def get(self, request, pk):
        # Checks for
        today = date.today()
        week_start = today - timedelta(days=today.isoweekday() % 7)

        report_data = {}

        queryset = Expense.objects.filter(user=self.request.user, date__range=[week_start, today])
        report_data.update({"expense_total": queryset.aggregate(Sum('value'))['value__sum']})

        category_data = {}
        category_set = Expense.objects.filter(user=self.request.user, date__range=[week_start, today]).values('category').distinct()

        # TODO: get type total to show properly
        for category in category_set:
            week_category_set = Expense.objects.filter(user=self.request.user, date__range=[week_start, today], category__iexact=category['category'])

            category_data.update({str(category['category']).lower(): week_category_set.aggregate(Sum('value'))['value__sum']})

            type_data = {}
            type_set = Expense.objects.filter(user=self.request.user, date__range=[week_start, today], category__iexact=category['category']).values('type').distinct()

            for type in type_set:

                week_type_set = Expense.objects.filter(user=self.request.user, date__range=[week_start, today], category__iexact=category['category'], type=type['type'])

                type_data.update({str(type['type']).lower(): week_type_set.aggregate(Sum('value'))['value__sum']})

            category_data.update({str(category['category']+'_type_total').lower(): type_data})

            print(category_data)
            print(" ")

        report_data.update({'category_total': category_data})

        return Response(data=report_data, status=status.HTTP_200_OK)
