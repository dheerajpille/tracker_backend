from django.conf.urls import url

from tracker_backend.trackerAPI.reports.views import *

urlpatterns = [
    # List of expenses from last week
    url(r'^weekly/$', WeeklyExpenseReport.as_view(), name='weekly-report'),

    # List of expenses from last month
    url(r'^monthly/$', MonthlyExpenseReport.as_view(), name='monthly-report'),

    # List of expenses from last year
    url(r'^yearly/$', YearlyExpenseReport.as_view(), name='yearly-report'),
]
