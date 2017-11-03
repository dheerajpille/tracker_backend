from django.conf.urls import url, include
from django.contrib import admin

from tracker_backend.trackerAPI.views import LoginView, SignupView

urlpatterns = [
    # Admin URL for Django
    url(r'^admin/', admin.site.urls),

    # Login and Signup calls for project
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^signup/$', SignupView.as_view(), name='signup'),

    # OAuth 2.0 verification for Django
    # Primarily used for o/token/, o/revoke_token/, and o/applications/
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    # URL for project's resources
    url(r'^tracker/', include('tracker_backend.trackerAPI.urls')),
]
