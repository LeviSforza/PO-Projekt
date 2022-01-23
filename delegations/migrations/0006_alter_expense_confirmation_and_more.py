# Generated by Django 4.0.1 on 2022-01-23 10:40

from django.db import migrations, models
import django.db.models.functions.datetime


class Migration(migrations.Migration):

    dependencies = [
        ('delegations', '0005_remove_advance_type_expense_title_expense_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='confirmation',
            field=models.FileField(blank=True, null=True, upload_to='expenses/'),
        ),
        migrations.AddConstraint(
            model_name='expense',
            constraint=models.CheckConstraint(check=models.Q(('date__lte', django.db.models.functions.datetime.Now())), name='correct_expense_date'),
        ),
    ]