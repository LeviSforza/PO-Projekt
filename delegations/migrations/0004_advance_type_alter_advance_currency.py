# Generated by Django 4.0.1 on 2022-01-22 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delegations', '0003_alter_expense_currency'),
    ]

    operations = [
        migrations.AddField(
            model_name='advance',
            name='type',
            field=models.CharField(choices=[('NOCLEG', 'NOCLEG'), ('WYZYWIENIE', 'WYZYWIENIE'), ('PRZEJAZD', 'PRZEJAZD'), ('KOSZTY DODATKOWE', 'KOSZTY DODATKOWE')], default='KOSZTY DODATKOWE', max_length=40),
        ),
        migrations.AlterField(
            model_name='advance',
            name='currency',
            field=models.CharField(choices=[('euro', 'euro'), ('zloty', 'zloty'), ('yen', 'yen'), ('british pound', 'british pound'), ('juan', 'juan'), ('swiss franc', 'swiss franc'), ('czech koruna', 'czech koruna'), ('american dollar', 'american dollar')], default='zloty', max_length=40),
        ),
    ]
