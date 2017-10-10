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
