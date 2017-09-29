from django.conf.urls import url, include
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from tracker_backend.trackerAPI.accounts.views import *

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^signup/$', SignupView.as_view(), name='signup'),
    url(r'^list/$', UserList.as_view(), name='list'),
    url(r'^user/(?P<pk>[0-9]+)/$', UserDetail.as_view(), name='userdetail'),

    # TODO: figure this out and implement it to login/other functions
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-refresh', refresh_jwt_token),
    url(r'^api-token-verify', verify_jwt_token),
]