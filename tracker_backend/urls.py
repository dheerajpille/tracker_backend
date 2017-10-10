"""tracker_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from tracker_backend.trackerAPI.views import LoginView, SignupView

urlpatterns = [
    # Admin URL for Django
    url(r'^admin/', admin.site.urls),

    # Login and Signup calls for Tracker
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^signup/$', SignupView.as_view(), name='signup'),

    # OAuth 2.0 verification for Django
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    # URL for project's resources
    url(r'^tracker/', include('tracker_backend.trackerAPI.urls')),
]
