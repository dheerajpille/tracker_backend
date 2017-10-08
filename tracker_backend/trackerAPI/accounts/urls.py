from django.conf.urls import url, include

from .views import *

urlpatterns = [
    # Add any URLs if needed

    url(r'^create/$', CreateExpense.as_view(), name='createExpense'),

    url(r'^expenselist/$', ExpenseList.as_view(), name='expenseList'),

    # User index, which directs to UserDetail view
    url(r'^$', UserDetail.as_view(), name='userDetail'),
]
