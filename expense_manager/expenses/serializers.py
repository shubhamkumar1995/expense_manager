from rest_framework import serializers
from .models import User, Expense, Balance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'isd_code']


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['amount', 'paid_by', 'description']


class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = ['user_owed', 'user_owes', 'amount']
