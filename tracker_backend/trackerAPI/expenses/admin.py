from django.contrib import admin

from tracker_backend.trackerAPI.expenses.models import Expense


class ExpenseAdmin(admin.ModelAdmin):
    """
    ExpenseAdmin, which displays the following fields in the expenses admin panel
    """

    # List of fields to be displayed in Expense admin panel
    list_display = ('date', 'user', 'category', 'type', 'value', 'currency', )


# Registers Expense model with ExpenseAdmin panel
admin.site.register(Expense, ExpenseAdmin)
