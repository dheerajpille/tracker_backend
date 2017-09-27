from django.conf.urls import url, include

from tracker_backend.trackerAPI.accounts import views as acc_views

urlpatterns = [
    url(r'^login/$', acc_views.LoginView.as_view(), name='login'),
    url(r'^signup/$', acc_views.SignupView.as_view(), name='signup'),
    url(r'^list/$', acc_views.UserList.as_view(), name='list'),
]