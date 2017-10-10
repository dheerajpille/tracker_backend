from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group


class UserAdmin(UserAdmin):
    """
    UserAdmin, which displays the following fields in the user's admin panel
    """

    list_display = ('id', 'username', 'first_name', 'last_name', 'email', )


# Unregisters standard User and Group admin panels
admin.site.unregister(User)
admin.site.unregister(Group)

# Registers standard User model to custom UserAdmin panel
admin.site.register(User, UserAdmin)
