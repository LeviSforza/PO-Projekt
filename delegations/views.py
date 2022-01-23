import datetime

from django.contrib.auth import (
    authenticate,
    login,
    logout
)
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils.dateparse import parse_date

from delegations.models import Delegation, Employee, UsersDelegations, Billing, BusinessExpenses, Expense
from .forms import UserLoginForm, DelegationForm, AddUsersForm, ExpenseForm


# Create your views here.


def index(request):
    return render(request, "index.html")


@login_required(login_url='/deleg/login/')
def delegations(request):
    global latest_question_list, role, delegat
    latest_question_list = []
    delegat = None

    if request.method == 'POST':
        if 'deleg' in request.POST:
            id_del = request.POST['deleg']
            delegat = Delegation.objects.get(id_delegation=id_del)
        if 'id_del' in request.POST:
            id_del = request.POST['id_del']
            delegation = Delegation.objects.get(id_delegation=id_del)
            delegation.delete()
            return redirect('/delegations/deleg')
        if 'cancel' in request.POST:
            return redirect('/delegations/deleg')

    if request.user.is_authenticated:
        employee = Employee.objects.get(pk=request.user.id)
        if employee.role == 'ORGANIZER':
            role = True
            latest_question_list = Delegation.objects.order_by('-id_delegation')
        else:
            role = False
            delegations_ids = UsersDelegations.objects.filter(FK_user=employee.id)
            for delegations_id in delegations_ids:
                latest_question_list.append(delegations_id.FK_delegation)

    context = {
        'delegations_list': latest_question_list,
        'user_role': role,
        'delegat': delegat,
    }
    return render(request, "delegations.html", context)


temp_delegation = Delegation()


@login_required(login_url='/deleg/login/')
def delegation(request, delegation_id):
    global form, expense_del, save, temp_delegation
    form = None
    expense_del = None
    save = False
    context = {}
    curr_delegation = Delegation.objects.get(pk=delegation_id)
    form = DelegationForm(instance=curr_delegation)
    participants_list = [curr_delegation.FK_organizer]
    for inst in UsersDelegations.objects.all():
        if inst.FK_delegation.id_delegation == delegation_id:
            participants_list.append(inst.FK_user)

    billing = Billing.objects.get(FK_delegation=curr_delegation)
    business_expenses = BusinessExpenses.objects.get(FK_billing=billing)
    expenses_list = []
    for exp in Expense.objects.all():
        if exp.FK_business_expenses == business_expenses:
            expenses_list.append(exp)

    if request.method == 'POST':
        if 'cancel' in request.POST:
            return redirect('/delegations/deleg')
        if 'cancel_stay' in request.POST:
            return redirect('/delegations/deleg/' + str(delegation_id))
        if 'save' in request.POST:
            save = True
            expense_del = None
            form = DelegationForm(request.POST)
            temp_delegation.departure_date = form['departure_date'].value()
            temp_delegation.return_date = form['return_date'].value()
            temp_delegation.base_currency = form['base_currency'].value()
            temp_delegation.duration = form['duration'].value()
            temp_delegation.country = form['country'].value()
        if 'save_delegation' in request.POST:
            curr_delegation.base_currency = temp_delegation.base_currency
            curr_delegation.duration = temp_delegation.duration
            curr_delegation.country = temp_delegation.country
            if temp_delegation.return_date >= temp_delegation.departure_date:
                curr_delegation.departure_date = temp_delegation.departure_date
                curr_delegation.return_date = temp_delegation.return_date
            curr_delegation.save()
            return redirect('/delegations/deleg/' + str(delegation_id))
        if 'delete_participant' in request.POST:
            id_delete = request.POST['delete_participant']
            user_delegation = UsersDelegations.objects.get(FK_user=id_delete, FK_delegation=delegation_id)
            user_delegation.delete()
            return redirect('/delegations/deleg/' + str(delegation_id))
        if 'delete_expense' in request.POST:
            id_delete = request.POST['delete_expense']
            expense_del = Expense.objects.get(id_expense=id_delete)
            save = False
        if 'id_expense_del' in request.POST:
            id_delete = request.POST['id_expense_del']
            expense = Expense.objects.get(id_expense=id_delete)
            expense.delete()
            return redirect('/delegations/deleg/' + str(delegation_id))

    context['form'] = form
    context['curr'] = curr_delegation
    context['save'] = save
    context['participants_list'] = participants_list
    context['expenses_list'] = expenses_list
    context['expense_del'] = expense_del
    return render(request, "details.html", context)


@login_required(login_url='/deleg/login/')
def add_delegation(request):
    global form
    form = None
    context = {}
    if request.method == 'POST':
        delegation = Delegation(FK_organizer=Employee.objects.get(pk=request.user.id))
        form = DelegationForm(request.POST or None, instance=delegation)

        if form.is_valid():
            form.save()
            billing = Billing.objects.create(
                FK_delegation=Delegation.objects.get(id_delegation=delegation.id_delegation))
            BusinessExpenses.objects.create(FK_billing=Billing.objects.get(id_billing=billing.id_billing))
            return redirect('/delegations/deleg')
    else:
        form = DelegationForm()

    context['form'] = form
    return render(request, "add_delegation.html", context)


@login_required(login_url='/deleg/login/')
def add_users(request, delegation_id):
    global form
    form = None
    context = {}
    if request.method == 'POST':
        users_delegations = UsersDelegations.objects.filter(
            FK_delegation=Delegation.objects.get(id_delegation=delegation_id))
        user_deleg_list = []
        for users_delegation in users_delegations:
            user_deleg_list.append(users_delegation.FK_user.id)
        print(user_deleg_list)
        form = AddUsersForm(request.POST or None)
        if form.is_valid():
            users = form.cleaned_data.get('users')
            to_add = []
            for user in users:
                if int(user) not in user_deleg_list:
                    to_add.append(user)
            for user in to_add:
                b = UsersDelegations(FK_user=Employee.objects.get(id=user),
                                     FK_delegation=Delegation.objects.get(id_delegation=delegation_id))
                b.save()
            return redirect('/delegations/deleg/' + str(delegation_id))
    else:
        form = AddUsersForm()

    context['form'] = form
    return render(request, "add_users.html", context)


@login_required(login_url='/deleg/login/')
def add_expense(request, delegation_id):
    global form
    form = None
    context = {}
    if request.method == 'POST':
        billing = Billing.objects.get(
            FK_delegation=Delegation.objects.get(id_delegation=delegation_id))
        expense = Expense(FK_business_expenses=BusinessExpenses.objects.get(
            FK_billing=billing))
        form = ExpenseForm(request.POST, request.FILES, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('/delegations/deleg/' + str(delegation_id))
    else:
        form = ExpenseForm()

    context['form'] = form
    return render(request, "add_expense.html", context)


def advance(request):
    return None


def login_view(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('/')

    context = {
        'form': form,
    }
    return render(request, "login.html", context)


def logout_view(request):
    logout(request)
    return redirect('/')
