from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Expense, Balance
from .serializers import UserSerializer, ExpenseSerializer, BalanceSerializer
from decimal import Decimal


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer


class AddExpenseEqualView(APIView):
    def post(self, request):
        data = request.data
        amount = Decimal(data['amount'])
        paid_by_id = data['paid_by']
        users_ids = data['users']
        description = data['description']

        paid_by = User.objects.get(id=paid_by_id)
        expense = Expense(amount=amount, paid_by=paid_by, description=description)
        expense.save()

        split_amount = round(amount / len(users_ids), 2)

        for user_id in users_ids:
            if user_id != paid_by_id:
                user_owes = User.objects.get(id=user_id)
                balance, created = Balance.objects.get_or_create(user_owed=paid_by, user_owes=user_owes)
                balance.amount += split_amount
                balance.amount = round(balance.amount, 2)
                balance.save()

        return Response({'message': 'Expense added and split equally successfully!'}, status=status.HTTP_201_CREATED)


class AddExpenseExactView(APIView):
    def post(self, request):
        data = request.data
        amount = Decimal(data['amount'])
        paid_by_id = data['paid_by']
        users_owed = data['users_owed']
        description = data['description']

        total_share = sum(Decimal(share) for share in users_owed.values())
        if total_share != amount:
            return Response({'error': 'Total shares do not match the total amount.'},
                            status=status.HTTP_400_BAD_REQUEST)

        paid_by = User.objects.get(id=paid_by_id)
        expense = Expense(amount=amount, paid_by=paid_by, description=description)
        expense.save()

        for user_id, exact_amount in users_owed.items():
            if user_id != paid_by_id:
                user_owes = User.objects.get(id=user_id)
                balance, created = Balance.objects.get_or_create(user_owed=paid_by, user_owes=user_owes)
                balance.amount += Decimal(exact_amount)
                balance.amount = round(balance.amount, 2)
                balance.save()

        return Response({'message': 'Expense added and split exactly successfully!'}, status=status.HTTP_201_CREATED)


class AddExpensePercentageView(APIView):
    def post(self, request):
        data = request.data
        amount = Decimal(data['amount'])
        paid_by_id = data['paid_by']
        users_percentage = data['users_percentage']
        description = data['description']

        total_percentage = sum(Decimal(percentage) for percentage in users_percentage.values())
        if total_percentage != 100:
            return Response({'error': 'Total percentage does not equal 100.'}, status=status.HTTP_400_BAD_REQUEST)

        paid_by = User.objects.get(id=paid_by_id)
        expense = Expense(amount=amount, paid_by=paid_by, description=description)
        expense.save()

        for user_id, percentage in users_percentage.items():
            exact_amount = round(amount * (Decimal(percentage) / 100), 2)
            if user_id != paid_by_id:
                user_owes = User.objects.get(id=user_id)
                balance, created = Balance.objects.get_or_create(user_owed=paid_by, user_owes=user_owes)
                balance.amount += exact_amount
                balance.amount = round(balance.amount, 2)
                balance.save()

        return Response({'message': 'Expense added and split by percentage successfully!'},
                        status=status.HTTP_201_CREATED)


class GetBalancesView(APIView):
    def get(self, request, user_id=None):
        if user_id:
            user = User.objects.get(id=user_id)
            balances_owed = Balance.objects.filter(user_owed=user, amount__gt=0)
            balances_owes = Balance.objects.filter(user_owes=user, amount__gt=0)
            balances = balances_owed | balances_owes
        else:
            balances = Balance.objects.filter(amount__gt=0)

        serializer = BalanceSerializer(balances, many=True)
        return Response(serializer.data)


class GetUserExpensesView(generics.ListAPIView):
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Expense.objects.filter(paid_by__id=user_id)
