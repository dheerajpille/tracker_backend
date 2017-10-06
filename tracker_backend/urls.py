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
from django.contrib.auth import views
from tracker_backend.trackerAPI.accounts.views import *

urlpatterns = [
    # Admin for Django
    url(r'^admin/', admin.site.urls),

    # TODO: remove this when not needed (soon)
    url(r'^login/$', LoginView.as_view(), name='login'),

    url(r'^signup/$', SignupView.as_view(), name='signup'),

    url(r'^list/$', UserList.as_view(), name='userList'),
    url(r'^user/(?P<pk>[0-9]+)/', UserDetail.as_view(), name='userDetail'),

    # TODO: change to addexpense View
    url(r'^user/(?P<pk>[0-9]+)/addexpense/$', CreateExpenseItem.as_view(), name='expenseDetail'),

    # TODO: configure authentication via OAuth
    # OAuth for Django
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    # URL for project's resources
    url(r'^tracker/', include('tracker_backend.trackerAPI.urls')),
]
