from django.conf.urls import url

from tracker_backend.trackerAPI.expenses.views import *

urlpatterns = [
    # Creates new Expense for current User
    url(r'^create/$', CreateExpenseView.as_view(), name='create-expense'),

    # List of all Expenses created for current User
    url(r'^list/$', ExpenseList.as_view(), name='expense-list'),

    # TODO: comment this
    url(r'^date/list/$', DateList.as_view(), name='date-list'),

    # TODO: comment this
    url(r'^category/list/$', CategoryList.as_view(), name='category-list'),

    # List of all Expenses created on a specified date
    url(r'^(?P<date>\d{4}-\d{2}-\d{2})/$', ExpenseDateList.as_view(), name='expense-date-list'),

    # List of all Expenses created for a certain category
    url(r'^(?P<category>\w{0,32})/$', ExpenseCategoryList.as_view(), name='expense-category-list'),

    # TODO: comment this
    url(r'^(?P<category>\w{0,32})/type/list/$', TypeList.as_view(), name='type-list'),

    # List of all Expenses created for a certain type in a certain category
    url(r'^(?P<category>\w{0,32})/(?P<type>\w{0,32})/$', ExpenseTypeList.as_view(), name='expenseTypeList'),

    # List of all Expenses created on a specified date for a specified category
    url(r'^(?P<date>\d{4}-\d{2}-\d{2})/(?P<category>\w{0,32})/$', ExpenseDateCategoryList.as_view()),

    # List of all Expenses created on a specified date for a specified type in a specified category
    # This results in the response being the only Expense that is specific enough to fit the criteria, due to the logic
    # behind the creation of Expense objects
    url(r'^(?P<date>\d{4}-\d{2}-\d{2})/(?P<category>\w{0,32})/(?P<type>\w{0,32})/$', ExpenseDetail.as_view()),



]
