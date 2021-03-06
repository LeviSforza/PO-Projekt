# Generated by Django 4.0.1 on 2022-01-22 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delegations', '0004_advance_type_alter_advance_currency'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='advance',
            name='type',
        ),
        migrations.AddField(
            model_name='expense',
            name='title',
            field=models.CharField(default='title', max_length=200),
        ),
        migrations.AddField(
            model_name='expense',
            name='type',
            field=models.CharField(choices=[('NOCLEG', 'NOCLEG'), ('WYZYWIENIE', 'WYZYWIENIE'), ('PRZEJAZD', 'PRZEJAZD'), ('KOSZTY DODATKOWE', 'KOSZTY DODATKOWE')], default='KOSZTY DODATKOWE', max_length=40),
        ),
    ]
