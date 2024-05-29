from celery import shared_task
from .models import User, Expense, Balance
import boto3
import csv
from django.conf import settings


@shared_task
def export_data_to_s3():
    users = User.objects.all()
    expenses = Expense.objects.all()
    balances = Balance.objects.all()

    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )

    # Export users
    user_file = '/tmp/users.csv'
    with open(user_file, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', 'Username', 'Email', 'Phone Number', 'ISD Code'])
        for user in users:
            writer.writerow([user.id, user.username, user.email, user.phone_number, user.isd_code])

    s3_client.upload_file(user_file, settings.AWS_STORAGE_BUCKET_NAME, 'users.csv')

    # Export expenses
    expense_file = '/tmp/expenses.csv'
    with open(expense_file, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', 'Amount', 'Paid By', 'Description'])
        for expense in expenses:
            writer.writerow([expense.id, expense.amount, expense.paid_by.id, expense.description])

    s3_client.upload_file(expense_file, settings.AWS_STORAGE_BUCKET_NAME, 'expenses.csv')

    # Export balances
    balance_file = '/tmp/balances.csv'
    with open(balance_file, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', 'User Owed', 'User Owes', 'Amount'])
        for balance in balances:
            writer.writerow([balance.id, balance.user_owed.id, balance.user_owes.id, balance.amount])

    s3_client.upload_file(balance_file, settings.AWS_STORAGE_BUCKET_NAME, 'balances.csv')
