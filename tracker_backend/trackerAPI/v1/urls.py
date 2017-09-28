from django.conf.urls import url, include

# TODO: add schema documentation here, if necessary
urlpatterns = [
    # TODO: change all these when porting to v1
    url(r'^', include('tracker_backend.trackerAPI.accounts.urls'), name='accounts'),

    # TODO: uncomment these once they have valid urls
    #url(r'^', include('tracker_backend.trackerAPI.expenses.urls'), name='expenses'),
    #url(r'^', include('tracker_backend.trackerAPI.reports.urls'), name='reports'),
]