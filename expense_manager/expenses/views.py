from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, Expense, Balance
from .serializers import UserSerializer, BalanceSerializer


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer


class AddExpenseEqualView(APIView):
    def post(self, request):
        data = request.data
        amount = data['amount']
        paid_by_id = data['paid_by']
        users_ids = data['users']
        description = data['description']

        paid_by = User.objects.get(id=paid_by_id)
        expense = Expense(amount=amount, paid_by=paid_by, description=description)
        expense.save()

        split_amount = amount / len(users_ids)

        for user_id in users_ids:
            if user_id != paid_by_id:
                user_owes = User.objects.get(id=user_id)
                balance, created = Balance.objects.get_or_create(user_owed=paid_by, user_owes=user_owes)
                balance.amount += split_amount
                balance.save()

        return Response({'message': 'Expense added and split equally successfully!'}, status=status.HTTP_201_CREATED)


class AddExpenseExactView(APIView):
    def post(self, request):
        data = request.data
        amount = data['amount']
        paid_by_id = data['paid_by']
        users_owed = data['users_owed']
        description = data['description']

        paid_by = User.objects.get(id=paid_by_id)
        expense = Expense(amount=amount, paid_by=paid_by, description=description)
        expense.save()

        for user_id, exact_amount in users_owed.items():
            if user_id != paid_by_id:
                user_owes = User.objects.get(id=user_id)
                balance, created = Balance.objects.get_or_create(user_owed=paid_by, user_owes=user_owes)
                balance.amount += exact_amount
                balance.save()

        return Response({'message': 'Expense added and split exactly successfully!'}, status=status.HTTP_201_CREATED)


class AddExpensePercentageView(APIView):
    def post(self, request):
        data = request.data
        amount = data['amount']
        paid_by_id = data['paid_by']
        users_percentage = data['users_percentage']
        description = data['description']

        paid_by = User.objects.get(id=paid_by_id)
        expense = Expense(amount=amount, paid_by=paid_by, description=description)
        expense.save()

        for user_id, percentage in users_percentage.items():
            exact_amount = amount * (percentage / 100)
            if user_id != paid_by_id:
                user_owes = User.objects.get(id=user_id)
                balance, created = Balance.objects.get_or_create(user_owed=paid_by, user_owes=user_owes)
                balance.amount += exact_amount
                balance.save()

        return Response({'message': 'Expense added and split by percentage successfully!'},
                        status=status.HTTP_201_CREATED)


class GetBalancesView(generics.ListAPIView):
    queryset = Balance.objects.all()
    serializer_class = BalanceSerializer
