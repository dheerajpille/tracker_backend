from django.conf.urls import url, include

from tracker_backend.trackerAPI.accounts.views import *

urlpatterns = [

    url(r'^user/', include('tracker_backend.trackerAPI.accounts.urls')),

    url(r'^userlist/$', UserList.as_view(), name='user-list'),
]