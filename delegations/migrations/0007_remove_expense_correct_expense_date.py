# Generated by Django 4.0.1 on 2022-01-23 10:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delegations', '0006_alter_expense_confirmation_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='expense',
            name='correct_expense_date',
        ),
    ]
