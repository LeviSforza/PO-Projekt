# Generated by Django 4.0.1 on 2022-01-29 00:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.expressions


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('username', models.CharField(max_length=60, unique=True)),
                ('first_name', models.CharField(max_length=60)),
                ('last_name', models.CharField(max_length=60)),
                ('role', models.CharField(choices=[('ORGANIZER', 'ORGANIZER'), ('PARTICIPANT', 'PARTICIPANT')],
                                          default='PARTICIPANT', max_length=20)),
                ('last_login', models.DateTimeField(auto_now=True)),
                ('admin', models.BooleanField(default=False)),
                ('staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Billing',
            fields=[
                ('id_billing', models.BigAutoField(primary_key=True, serialize=False)),
                ('returnable_sum', models.DecimalField(decimal_places=2, default=0.0, max_digits=20, null=True)),
                ('unreturnable_sum', models.DecimalField(decimal_places=2, default=0.0, max_digits=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BusinessExpenses',
            fields=[
                ('id_business_expenses', models.BigAutoField(primary_key=True, serialize=False)),
                ('basic_expenses', models.DecimalField(decimal_places=2, default=0.0, max_digits=20, null=True)),
                ('additional_expenses', models.DecimalField(decimal_places=2, default=0.0, max_digits=20, null=True)),
                ('FK_billing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                                 to='delegations.billing')),
            ],
        ),
        migrations.CreateModel(
            name='Delegation',
            fields=[
                ('id_delegation', models.BigAutoField(primary_key=True, serialize=False)),
                ('departure_date', models.DateField()),
                ('return_date', models.DateField()),
                ('country', models.CharField(max_length=45)),
                ('status', models.CharField(choices=[('new', 'new'), ('valid', 'valid'), ('ended', 'ended'),
                                                     ('paidoff', 'paidoff')], default='new', max_length=20)),
                ('base_currency', models.CharField(choices=[('euro', 'euro'), ('zloty', 'zloty'), ('yen', 'yen'),
                                                            ('british pound', 'british pound'), ('juan', 'juan'), ('swiss franc', 'swiss franc'), ('czech koruna', 'czech koruna'), ('american dollar', 'american dollar')], default='zloty', max_length=30)),
                ('duration', models.IntegerField(default=0)),
                ('FK_organizer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL,
                                                   to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UsersDelegations',
            fields=[
                ('id_users_delegations', models.BigAutoField(primary_key=True, serialize=False)),
                ('FK_delegation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                                    to='delegations.delegation')),
                ('FK_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                              to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id_expense', models.BigAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(default='title', max_length=200)),
                ('date', models.DateField()),
                ('type', models.CharField(choices=[('NOCLEG', 'NOCLEG'), ('WYZYWIENIE', 'WYZYWIENIE'),
                                                   ('PRZEJAZD', 'PRZEJAZD'), ('KOSZTY DODATKOWE', 'KOSZTY DODATKOWE')],
                                          default='KOSZTY DODATKOWE', max_length=40)),
                ('sum', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('currency', models.CharField(choices=[('euro', 'euro'), ('zloty', 'zloty'), ('yen', 'yen'),
                                                       ('british pound', 'british pound'), ('juan', 'juan'),
                                                       ('swiss franc', 'swiss franc'), ('czech koruna', 'czech koruna'),
                                                       ('american dollar', 'american dollar')],
                                              default='zloty', max_length=30)),
                ('confirmation', models.FileField(blank=True, null=True, upload_to='expenses/')),
                ('FK_business_expenses', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                                           to='delegations.businessexpenses')),
            ],
        ),
        migrations.AddField(
            model_name='billing',
            name='FK_delegation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='delegations.delegation'),
        ),
        migrations.CreateModel(
            name='Advance',
            fields=[
                ('id_advance', models.BigAutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('advance_sum', models.DecimalField(decimal_places=2, default=0.0, max_digits=20, null=True)),
                ('currency', models.CharField(choices=[('euro', 'euro'), ('zloty', 'zloty'), ('yen', 'yen'),
                                                       ('british pound', 'british pound'), ('juan', 'juan'),
                                                       ('swiss franc', 'swiss franc'), ('czech koruna', 'czech koruna'),
                                                       ('american dollar', 'american dollar')],
                                              default='zloty', max_length=40)),
                ('confirmation', models.FileField(blank=True, null=True, upload_to='uploads/advance/% Y/% m/% d/')),
                ('FK_billing', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL,
                                                 to='delegations.billing')),
            ],
        ),
        migrations.AddConstraint(
            model_name='delegation',
            constraint=models.CheckConstraint(check=models.Q(('return_date__gte',
                                                              django.db.models.expressions.F('departure_date'))),
                                              name='check_start_date'),
        ),
    ]
