from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from tracker_backend.trackerAPI.accounts.models import User

# Register your models here.
class UserAdmin(UserAdmin):
    """
    UserAdmin, which controls the display of user values on administration panel
    """

    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'budget', )


admin.site.register(User, UserAdmin)
