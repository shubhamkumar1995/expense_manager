# Generated by Django 3.2.13 on 2024-05-29 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0002_alter_balance_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='balance',
            name='amount',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
