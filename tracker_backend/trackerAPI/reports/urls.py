from django.conf.urls import url, include

from tracker_backend.trackerAPI.reports.views import *

urlpatterns = [

    url(r'^weeklyreport/$', WeeklyExpenseList.as_view(), name='userDetail'),

    url(r'^monthlyreport/', MonthlyExpenseList.as_view()),

    url(r'^yearlyreport/', YearlyExpenseList.as_view()),
]