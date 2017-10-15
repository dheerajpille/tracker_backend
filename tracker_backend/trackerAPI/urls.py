from django.conf.urls import url, include

from tracker_backend.trackerAPI.utils import documentation
from tracker_backend.trackerAPI.views import UserDetail, UserList

urlpatterns = [
    url(r'^documentation/$', documentation, name='documentation'),

    # User detail based on pk/id value
    url(r'^user/(?P<pk>[0-9]+)/$', UserDetail.as_view(), name='user-detail'),

    # User list in database, only accessible to superuser/admin accounts
    url(r'^user/list/$', UserList.as_view(), name='user-list'),

    # Leads to expense application
    url(r'^user/(?P<pk>[0-9]+)/expense/', include('tracker_backend.trackerAPI.expenses.urls'),
        name='expense-application'),

    # Leads to report application
    url(r'^user/(?P<pk>[0-9]+)/report/', include('tracker_backend.trackerAPI.reports.urls'),
        name='report-application'),
]
