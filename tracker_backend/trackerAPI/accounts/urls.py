from django.conf.urls import url, include

from .views import *

urlpatterns = [
    # Add any URLs if needed

    # User index, which directs to UserDetail view
    url(r'^$', UserDetail.as_view(), name='userDetail'),

    # Creates an expense for current User with given details
    url(r'^create/$', CreateExpense.as_view(), name='createExpense'),

    # Gets all expenses ever created for a user
    url(r'^expenselist/$', ExpenseList.as_view(), name='expenseList'),

    # TODO: configure this for report
    url(r'^report/', include('tracker_backend.trackerAPI.reports.urls')),
]
