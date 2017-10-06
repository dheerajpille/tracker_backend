from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, ExpenseItem


# Register your models here.
class UserAdmin(UserAdmin):
    """
    UserAdmin, which controls the display of user values on administration panel
    """

    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'budget', )


class ExpenseItemAdmin(admin.ModelAdmin):
    list_display = ('date', 'category', 'type', 'value', 'currency', )


admin.site.register(User, UserAdmin)
admin.site.register(ExpenseItem, ExpenseItemAdmin)
