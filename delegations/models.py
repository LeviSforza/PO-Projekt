from enum import Enum

from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from decimal import Decimal

from django.db.models import CheckConstraint, Q, F
from django.db.models.functions import Now


class MyWorkerManager(BaseUserManager):

    def create_user(self, username, first_name, last_name, password=None):
        if not username:
            raise ValueError('Username is required!')
        if not first_name:
            raise ValueError('first_name is required!')
        if not last_name:
            raise ValueError('last_name is required!')
        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, first_name, last_name, password):
        if not username:
            raise ValueError('Username is required!')
        if not first_name:
            raise ValueError('first_name is required!')
        if not last_name:
            raise ValueError('last_name is required!')
        user = self.create_user(
            username,
            first_name,
            last_name,
            password=password
        )
        user.admin = True
        user.staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Employee(AbstractBaseUser):
    ORGANIZER = 'ORGANIZER'
    PARTICIPANT = 'PARTICIPANT'
    ADMIN = 'Admin'

    ROLES = (
        (ORGANIZER, ORGANIZER),
        (PARTICIPANT, PARTICIPANT),
    )

    username = models.CharField(max_length=60, unique=True)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    role = models.CharField(max_length=20, choices=ROLES, default=PARTICIPANT)
    last_login = models.DateTimeField(auto_now=True)
    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = MyWorkerManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def get_employee(self):
        return self

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return self.admin

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin


class Delegation(models.Model):
    NEW = 'new'
    ENDED = 'ended'
    PAIDOFF = 'paidoff'
    VALID = 'valid'

    STATUS = (
        (NEW, NEW),
        (VALID, VALID),
        (ENDED, ENDED),
        (PAIDOFF, PAIDOFF),
    )

    EURO = 'euro'
    ZLOTY = 'zloty'
    YEN = 'yen'
    POUND = 'british pound'
    JUAN = 'juan'
    FRANC = 'swiss franc'
    KORUNA = 'czech koruna'
    DOLLAR = 'american dollar'

    CURRENCY = (
        (EURO, EURO),
        (ZLOTY, ZLOTY),
        (YEN, YEN),
        (POUND, POUND),
        (JUAN, JUAN),
        (FRANC, FRANC),
        (KORUNA, KORUNA),
        (DOLLAR, DOLLAR),
    )

    id_delegation = models.BigAutoField(primary_key=True)
    departure_date = models.DateField()
    return_date = models.DateField()
    country = models.CharField(max_length=45)
    status = models.CharField(max_length=255, choices=STATUS, default=NEW)
    base_currency = models.CharField(max_length=255, choices=CURRENCY, default=ZLOTY)
    duration = models.IntegerField(default=0)
    FK_organizer = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(return_date__gte=F('departure_date')),
                name='check_start_date',
            ),
        ]


class Billing(models.Model):
    id_billing = models.BigAutoField(primary_key=True)
    returnable_sum = models.DecimalField(default=0.0, decimal_places=2, null=True, max_digits=20)
    unreturnable_sum = models.DecimalField(default=0.0, decimal_places=2, null=True, max_digits=20)
    FK_delegation = models.ForeignKey(Delegation, on_delete=models.CASCADE)


class BusinessExpenses(models.Model):
    id_business_expenses = models.BigAutoField(primary_key=True)
    basic_expenses = models.DecimalField(default=0.0, decimal_places=2, null=True, max_digits=20)
    additional_expenses = models.DecimalField(default=0.0, decimal_places=2, null=True, max_digits=20)
    FK_billing = models.ForeignKey(Billing, on_delete=models.CASCADE)


class UsersDelegations(models.Model):
    id_users_delegations = models.BigAutoField(primary_key=True)
    FK_user = models.ForeignKey(Employee, on_delete=models.CASCADE)
    FK_delegation = models.ForeignKey(Delegation, on_delete=models.CASCADE)


class Expense(models.Model):
    EURO = 'euro'
    ZLOTY = 'zloty'
    YEN = 'yen'
    POUND = 'british pound'
    JUAN = 'juan'
    FRANC = 'swiss franc'
    KORUNA = 'czech koruna'
    DOLLAR = 'american dollar'

    CURRENCY = (
        (EURO, EURO),
        (ZLOTY, ZLOTY),
        (YEN, YEN),
        (POUND, POUND),
        (JUAN, JUAN),
        (FRANC, FRANC),
        (KORUNA, KORUNA),
        (DOLLAR, DOLLAR),
    )

    ACCOMMODATION = 'NOCLEG'
    BOARD = 'WYZYWIENIE'
    TRANSFER = 'PRZEJAZD'
    ADDITIONAL = 'KOSZTY DODATKOWE'

    TYPE = (
        (ACCOMMODATION, ACCOMMODATION),
        (BOARD, BOARD),
        (TRANSFER, TRANSFER),
        (ADDITIONAL, ADDITIONAL),
    )

    id_expense = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=200, default='title')
    date = models.DateField()
    type = models.CharField(max_length=40, choices=TYPE, default=ADDITIONAL)
    sum = models.DecimalField(default=0.0, decimal_places=2, max_digits=20)
    currency = models.CharField(max_length=255, choices=CURRENCY, default=ZLOTY)
    confirmation = models.FileField(upload_to='expenses/', blank=True, null=True)
    FK_business_expenses = models.ForeignKey(BusinessExpenses, on_delete=models.CASCADE)


class Advance(models.Model):
    EURO = 'euro'
    ZLOTY = 'zloty'
    YEN = 'yen'
    POUND = 'british pound'
    JUAN = 'juan'
    FRANC = 'swiss franc'
    KORUNA = 'czech koruna'
    DOLLAR = 'american dollar'

    CURRENCY = (
        (EURO, EURO),
        (ZLOTY, ZLOTY),
        (YEN, YEN),
        (POUND, POUND),
        (JUAN, JUAN),
        (FRANC, FRANC),
        (KORUNA, KORUNA),
        (DOLLAR, DOLLAR),
    )

    id_advance = models.BigAutoField(primary_key=True)
    date = models.DateField()
    advance_sum = models.DecimalField(default=0.0, decimal_places=2, null=True, max_digits=20)
    currency = models.CharField(max_length=40, choices=CURRENCY, default=ZLOTY)
    confirmation = models.FileField(upload_to='uploads/advance/% Y/% m/% d/', blank=True, null=True)
    FK_billing = models.ForeignKey(Billing, on_delete=models.SET_NULL, null=True)
