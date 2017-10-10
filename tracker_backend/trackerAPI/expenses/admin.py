from django.contrib import admin

from tracker_backend.trackerAPI.expenses.models import Expense

# Register your models here.


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('date', 'user', 'category', 'type', 'value', 'currency', )


admin.site.register(Expense, ExpenseAdmin)
