from datetime import datetime

from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model

)
from django.core.exceptions import ValidationError
from django.forms import widgets
from delegations.models import Delegation, Employee, UsersDelegations, Expense

User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('This user does not exist')
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect password')
            if not user.is_active:
                raise forms.ValidationError('This user is not active')
        return super(UserLoginForm, self).clean(*args, **kwargs)


class DateTimePickerInput(forms.DateTimeInput):
    input_type = 'datetime'


class DelegationForm(forms.ModelForm):
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

    departure_date = forms.DateField(widget=widgets.DateInput(format='%Y-%m-%d', attrs={'type': 'date',
                                                                                        'data-provide': 'datepicker',
                                                                                        'data-date-format': 'yyyy-mm-dd'}))
    return_date = forms.DateField(widget=widgets.DateInput(format='%Y-%m-%d', attrs={'type': 'date',
                                                                                     'data-provide': 'datepicker',
                                                                                     'data-date-format': 'yyyy-mm-dd'}))
    country = forms.CharField(max_length=45)
    base_currency = forms.ChoiceField(choices=CURRENCY, required=True)
    duration = forms.IntegerField()

    def clean(self):
        cleaned_data = super().clean()
        departure_date = cleaned_data.get("departure_date")
        return_date = cleaned_data.get("return_date")
        duration = cleaned_data.get("duration")

        if departure_date and return_date:
            if departure_date > return_date:
                raise ValidationError(
                    "Wprowadzone dane są niepoprawne! "
                    "Data powrotu nie może być wcześniejsza od daty wyjazdu!!!"
                )

        if duration:
            if duration < 0:
                raise ValidationError(
                    "Wprowadzone dane są niepoprawne! "
                    "Czas trwania wyjazdu nie może być mniejszy od 0!!!"
                )

    class Meta:
        model = Delegation
        exclude = ['status', 'FK_organizer']
        widgets = {
            'departure_date': widgets.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'return_date': widgets.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }


class AddUsersForm(forms.Form):
    employees = Employee.objects.filter(role='PARTICIPANT')
    participants = []
    for employee in employees:
        participant = (employee.id, str(employee.id) + " - " + str(employee.last_name) + " " + \
                       str(employee.first_name) + " - " + str(employee.username))
        participants.append(participant)
    users = forms.MultipleChoiceField(choices=participants,
                                      widget=forms.CheckboxSelectMultiple())


# create a ModelForm
class ExpenseForm(forms.ModelForm):
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

    title = forms.CharField(max_length=45)
    date = forms.DateField(widget=widgets.DateInput(format='%Y-%m-%d', attrs={'type': 'date',
                                                                              'data-provide': 'datepicker',
                                                                              'data-date-format': 'yyyy-mm-dd'}))
    type = forms.ChoiceField(choices=TYPE, required=True)
    sum = forms.DecimalField(decimal_places=2, max_digits=20)
    currency = forms.ChoiceField(choices=CURRENCY, required=True)
    confirmation = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': False}), required=False)

    class Meta:
        model = Expense
        exclude = ['FK_business_expenses']
        widgets = {
            'date': widgets.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }
