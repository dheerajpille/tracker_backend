from django.conf.urls import url, include

from tracker_backend.trackerAPI.accounts.views import *

urlpatterns = [
    # url(r'^v1/', include('tracker_backend.trackerAPI.v1.urls')),

    url(r'^list/$', UserList.as_view(), name='userList'),
    url(r'^user/(?P<pk>[0-9]+)/', UserDetail.as_view(), name='userDetail'),
    url(r'^doom/$', CreateExpenseItem.as_view(), name='expense'),
    url(r'^expenselist/$', ExpenseList.as_view(), name='expenseList'),
]