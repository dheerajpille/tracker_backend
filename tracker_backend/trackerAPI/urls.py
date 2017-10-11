from django.conf.urls import url, include

from tracker_backend.trackerAPI.views import UserDetail, UserList

urlpatterns = [
    # User detail derived from pk/id
    url(r'^user/(?P<pk>[0-9]+)/$', UserDetail.as_view(), name='user-detail'),

    # Registered user list in database, only accessible by superuser/admin
    url(r'^userlist/$', UserList.as_view(), name='user-list'),

    # Lead to expense application
    url(r'^user/(?P<pk>[0-9]+)/expense/', include('tracker_backend.trackerAPI.expenses.urls')),

    # Lead to report application
    url(r'^user/(?P<pk>[0-9]+)/report/', include('tracker_backend.trackerAPI.reports.urls')),
]
