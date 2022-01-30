import datetime

from django.db import IntegrityError
from django.test import TestCase

from delegations.forms import ExpenseForm
from delegations.models import Delegation, Employee, Billing, BusinessExpenses, Expense


class ExpenseFormTest(TestCase):
    def test_expense_form_date_field_help_text(self):
        form = ExpenseForm()
        self.assertTrue(
            form.fields['date'].help_text == 'Data nie może być późniejsza od dzisiejszej')

    # common case
    def test_expense_form_date_correct_data(self):
        date = datetime.date.today() - datetime.timedelta(days=10)
        form = ExpenseForm(data={'title': 'test', 'date': date, 'type': 'NOCLEG', 'sum': 0, 'currency': 'euro'})
        self.assertTrue(form.is_valid())

    # common case
    def test_expense_form_date_incorrect_data(self):
        date = datetime.date.today() + datetime.timedelta(days=10)
        form = ExpenseForm(data={'title': 'test', 'date': date, 'type': 'NOCLEG', 'sum': 0, 'currency': 'euro'})
        self.assertFalse(form.is_valid())

    # edge case
    def test_expense_form_date_one_day_in_the_past(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        form = ExpenseForm(data={'title': 'test', 'date': date, 'type': 'NOCLEG', 'sum': 0, 'currency': 'euro'})
        self.assertTrue(form.is_valid())

    # edge case
    def test_expense_form_date_today(self):
        date = datetime.date.today()
        form = ExpenseForm(data={'title': 'test', 'date': date, 'type': 'NOCLEG', 'sum': 0, 'currency': 'euro'})
        self.assertTrue(form.is_valid())

    # edge case
    def test_expense_form_date_one_day_in_the_future(self):
        date = datetime.date.today() + datetime.timedelta(days=1)
        form = ExpenseForm(data={'title': 'test', 'date': date, 'type': 'NOCLEG', 'sum': 0, 'currency': 'euro'})
        self.assertFalse(form.is_valid())


class DelegationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Employee.objects.create(username='organizer', first_name='Anna', last_name='Jantar',
                                password='p@ss', role='ORGANIZER')
        Delegation.objects.create(departure_date='2022-01-21', return_date='2022-01-29', country='Polska',
                                  duration=8, FK_organizer=Employee.objects.get(id=1))
        Delegation.objects.get(id_delegation=1).createDelegationsCompanionObjects()

    def test_country_max_length(self):
        delegation = Delegation.objects.get(id_delegation=1)
        max_length = delegation._meta.get_field('country').max_length
        self.assertEqual(max_length, 45)

    def test_status_max_length(self):
        delegation = Delegation.objects.get(id_delegation=1)
        max_length = delegation._meta.get_field('status').max_length
        self.assertEqual(max_length, 20)

    def test_base_currency_max_length(self):
        delegation = Delegation.objects.get(id_delegation=1)
        max_length = delegation._meta.get_field('base_currency').max_length
        self.assertEqual(max_length, 30)

    def test_str_call(self):
        delegation = Delegation.objects.get(id_delegation=1)
        self.assertEqual('2022-01-21 - 2022-01-29 - Polska', str(delegation))

    def test_departure_return_dates_constraint_same_dates(self):
        delegation2 = Delegation(departure_date='2022-01-01', return_date='2022-01-01', country='Polska',
                                 FK_organizer=Employee.objects.get(id=1))
        delegation2.save()
        self.assertEqual(delegation2, Delegation.objects.get(id_delegation=2))

    def test_departure_return_dates_constraint_error(self):
        with self.assertRaises(Exception) as raised:
            Delegation.objects.create(departure_date='2022-01-02',
                                      return_date='2022-01-01', country='Polska',
                                      FK_organizer=Employee.objects.get(id=1))
        self.assertEqual(IntegrityError, type(raised.exception))

    def test_create_delegations_companion_objects(self):
        delegation = Delegation.objects.get(id_delegation=1)
        billing = Billing.objects.get(FK_delegation=delegation)
        business_expenses = BusinessExpenses.objects.get(FK_billing=billing)
        self.assertEqual(Billing.objects.get(id_billing=1), billing)
        self.assertEqual(BusinessExpenses.objects.get(id_business_expenses=1), business_expenses)

    def test_get_billing(self):
        delegation = Delegation.objects.get(id_delegation=1)
        billing = delegation.getBilling()
        self.assertEqual(Billing.objects.get(id_billing=1), billing)

    def test_get_business_expenses(self):
        delegation = Delegation.objects.get(id_delegation=1)
        business_expenses = delegation.getBusinessExpenses()
        self.assertEqual(BusinessExpenses.objects.get(id_business_expenses=1), business_expenses)

    def test_get_expenses_none(self):
        delegation = Delegation.objects.get(id_delegation=1)
        expenses = delegation.getExpenses()
        self.assertEqual([], expenses)

    def test_get_expenses_one(self):
        delegation = Delegation.objects.get(id_delegation=1)
        Expense.objects.create(title='test', date='2022-01-01', FK_business_expenses=delegation.getBusinessExpenses())
        expenses = delegation.getExpenses()
        self.assertEqual(1, len(expenses))

    def test_get_expenses_many(self):
        delegation = Delegation.objects.get(id_delegation=1)
        for x in range(20):
            Expense.objects.create(title='test' + str(x), date='2022-01-01',
                                   FK_business_expenses=delegation.getBusinessExpenses())
        expenses = delegation.getExpenses()
        self.assertEqual(20, len(expenses))
