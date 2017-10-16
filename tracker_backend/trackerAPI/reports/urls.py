from django.conf.urls import url

from tracker_backend.trackerAPI.reports.views import DailyReport, WeeklyReport, MonthlyReport, YearlyReport


urlpatterns = [
    # Report of expenses in today
    url(r'^daily/$', DailyReport.as_view(), name='daily-report'),

    # Report of expenses in current week
    url(r'^weekly/$', WeeklyReport.as_view(), name='weekly-report'),

    # Report of expenses in current month
    url(r'^monthly/$', MonthlyReport.as_view(), name='monthly-report'),

    # Report of expenses in current year
    url(r'^yearly/$', YearlyReport.as_view(), name='yearly-report'),
]
