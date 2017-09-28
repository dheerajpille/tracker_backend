from django.conf.urls import url, include

from tracker_backend.trackerAPI.accounts import views as acc_views

urlpatterns = [
    url(r'^v1/', include('tracker_backend.trackerAPI.v1.urls')),
]