from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    isd_code = models.CharField(max_length=15)

    def __str__(self):
        return self.username


class Expense(models.Model):
    amount = models.FloatField()
    paid_by = models.ForeignKey(User, related_name='paid_expenses', on_delete=models.CASCADE)
    description = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.description}: {self.amount}"


class Balance(models.Model):
    user_owed = models.ForeignKey(User, related_name='owed_balances', on_delete=models.CASCADE)
    user_owes = models.ForeignKey(User, related_name='owes_balances', on_delete=models.CASCADE)
    amount = models.FloatField(null=True, blank=True, default=0)

    def __str__(self):
        return f"{self.user_owes} owes {self.user_owed}: {self.amount}"
