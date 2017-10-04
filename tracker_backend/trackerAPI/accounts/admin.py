from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


# Register your models here.
class UserAdmin(UserAdmin):
    """
    UserAdmin, which controls the display of user values on administration panel
    """

    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'budget', 'currency', )


admin.site.register(User, UserAdmin)
