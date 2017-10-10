from django.conf.urls import url, include

from tracker_backend.trackerAPI.accounts.views import *

urlpatterns = [
    # url(r'^v1/', include('tracker_backend.trackerAPI.v1.urls')),

    # Base level URLs for API
    # Leads to basic user functionality views
    url(r'^user/(?P<pk>[0-9]+)/', include('tracker_backend.trackerAPI.accounts.urls')),

    # Gets the registered user list for superuser access only
    url(r'^userlist/$', UserList.as_view(), name='userList'),
]