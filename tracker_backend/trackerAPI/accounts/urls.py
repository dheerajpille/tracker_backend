from django.conf.urls import url, include

from tracker_backend.trackerAPI.accounts.views import *

urlpatterns = [

    url(r'^(?P<pk>[0-9]+)/$', UserDetail.as_view(), name='userDetail'),

    url(r'^(?P<pk>[0-9]+)/expense/', include('tracker_backend.trackerAPI.expenses.urls')),

    url(r'^(?P<pk>[0-9]+)/report/', include('tracker_backend.trackerAPI.reports.urls')),
]
