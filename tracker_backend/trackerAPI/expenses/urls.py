from django.conf.urls import url, include

from .views import *

urlpatterns = [
    # Creates an expense for current User with given details
    url(r'^create/$', POSTExpense.as_view(), name='post-expense'),

    # Gets all expenses ever created for a user
    url(r'^expenselist/$', ExpenseList.as_view(), name='expense-list'),

    # TODO: configure this for reporting purposes
    url(r'^(?P<date>\d{4}-\d{2}-\d{2})/$', ExpenseDateList.as_view(), name='expenseDateList'),

    # TODO: comment these
    url(r'^(?P<date>\d{4}-\d{2}-\d{2})/(?P<category>\w{0,32})/$', ExpenseDateCategoryList.as_view()),
    url(r'^(?P<date>\d{4}-\d{2}-\d{2})/(?P<category>\w{0,32})/(?P<type>\w{0,32})/$', ExpenseDateTypeList.as_view()),

    # TODO: also figure this out, please and thank you!
    # Category expense list
    url(r'^(?P<category>\w{0,32})/$', ExpenseCategoryList.as_view(), name='expenseCategoryList'),

    # Type expense list
    url(r'^(?P<category>\w{0,32})/(?P<type>\w{0,32})/$', ExpenseTypeList.as_view(), name='expenseTypeList'),
]
