from rest_framework import serializers

from tracker_backend.trackerAPI.serializers import UserSerializer
from tracker_backend.trackerAPI.expenses.models import Expense


class ExpenseSerializer(serializers.ModelSerializer):
    """
    Standard serializer for expense model
    """

    # TODO: change this to be default/required=False
    date = serializers.DateField(required=True)

    # TODO: hide this from response body
    user = UserSerializer(read_only=True, required=False)

    category = serializers.CharField(max_length=32, required=True)
    type = serializers.CharField(max_length=32, required=True)
    value = serializers.DecimalField(max_digits=8, decimal_places=2, required=True)

    # TODO: same here
    currency = serializers.CharField(max_length=3, required=False)

    # Creates Expense object with POST data
    def create(self, validated_data):

        # Determines each field from given POST data
        date = self.validated_data['date']
        user = self.context['request'].user
        category = self.validated_data['category']
        type = self.validated_data['type']
        value = self.validated_data['value']
        currency = self.validated_data['currency']

        # Creates the Expense object with aforementioned validated data
        expense = Expense.objects.create(date=date, user=user, category=category, type=type, value=value,
                                         currency=currency, )
        expense.save()

        # Returns the Expense's data as JSON response and saves it to database
        return expense

    class Meta:
        # Specifies model
        model = Expense

        # List of fields that were shown in JSON response
        fields = ('date', 'user', 'category', 'type', 'value', 'currency', )

        # TODO: determine whether to delete this or not
        depth = 1
