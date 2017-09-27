from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class UserAdmin(UserAdmin):
    """
    UserAdmin, which controls the display of user values on administration panel
    """
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'income', 'password', )

admin.site.register(get_user_model(), UserAdmin)
