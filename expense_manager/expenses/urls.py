from django.contrib import admin
from django.urls import path
from .views import UserCreateView, AddExpenseEqualView, AddExpenseExactView, AddExpensePercentageView, GetBalancesView

urlpatterns = [
    path('users/', UserCreateView.as_view(), name='add_user'),
    path('expenses/equal/', AddExpenseEqualView.as_view(), name='add_expense_equal'),
    path('expenses/exact/', AddExpenseExactView.as_view(), name='add_expense_exact'),
    path('expenses/percentage/', AddExpensePercentageView.as_view(), name='add_expense_percentage'),
    path('balances/', GetBalancesView.as_view(), name='get_balances'),
]