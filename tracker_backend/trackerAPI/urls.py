from django.conf.urls import url, include

from tracker_backend.trackerAPI.accounts import views as acc_views

urlpatterns = [
    url(r'^login/$', acc_views.LoginView.as_view(), name='login'),
]