from rest_framework import serializers

from tracker_backend.trackerAPI.expenses.models import Expense
from tracker_backend.trackerAPI.accounts.serializers import UserSerializer


class ExpenseSerializer(serializers.ModelSerializer):
    """
    Standard serializer for expense model
    """
    date = serializers.DateField(required=False)

    user = UserSerializer(read_only=True, required=False)

    category = serializers.CharField(max_length=32, required=True)
    type = serializers.CharField(max_length=32, required=True)
    value = serializers.DecimalField(max_digits=8, decimal_places=2, required=True)
    currency = serializers.CharField(max_length=3, required=False)

    def create(self, validated_data):
        date = self.validated_data['date']

        user = self.context['request'].user

        category = self.validated_data['category']
        type = self.validated_data['type']
        value = self.validated_data['value']
        currency = self.validated_data['currency']

        expense = Expense.objects.create(date=date, user=user, category=category, type=type, value=value,
                                         currency=currency, )
        expense.save()

        return expense

    class Meta:
        model = Expense
        fields = ('date', 'user', 'category', 'type', 'value', 'currency', )
        depth = 1
