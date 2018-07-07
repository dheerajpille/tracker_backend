from datetime import date as import_date

from rest_framework import serializers

from tracker_backend.trackerAPI.expenses.models import Expense


class ExpenseSerializer(serializers.ModelSerializer):
    """
    Standard serializer for expense model
    """

    # Determines each fields types and defaults, if applicable
    date = serializers.DateField(required=False, default=import_date.today())
    category = serializers.CharField(max_length=32, required=True)
    type = serializers.CharField(max_length=32, required=True)
    value = serializers.DecimalField(max_digits=8, decimal_places=2, required=True)

    # Creates Expense object with POST data
    def create(self, validated_data):

        # Determines each field from given POST data or defaults
        date = self.validated_data['date'] or import_date.today()
        user = self.context['request'].user
        category = self.validated_data['category']
        type = self.validated_data['type']
        value = self.validated_data['value']

        # Creates the Expense object with aforementioned validated data
        expense = Expense.objects.create(date=date, user=user, category=category, type=type, value=value, )

        expense.save()

        # Returns the Expense's data as JSON response and saves it to database
        return expense

    class Meta:

        # Specifies model
        model = Expense

        # List of fields that were shown in JSON response
        fields = ('date', 'category', 'type', 'value', )
