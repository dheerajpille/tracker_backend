from django.conf.urls import url, include

from tracker_backend.trackerAPI.accounts.views import *

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^signup/$', SignupView.as_view(), name='signup'),
    url(r'^list/$', UserList.as_view(), name='list'),
]