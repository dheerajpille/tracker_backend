from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.


class UserAdmin(UserAdmin):
    """
    UserAdmin, which controls the display of user values on administration panel
    """

    list_display = ('id', 'username', 'first_name', 'last_name', 'email', )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
