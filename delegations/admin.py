from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User
from delegations.models import Billing, Delegation, Expense, UsersDelegations, BusinessExpenses, Advance
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Employee


class AccountAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'role')
    search_fields = ('username', 'first_name', 'last_name')
    readonly_field = 'id'
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Employee, AccountAdmin)
admin.site.register(Billing)
admin.site.register(Delegation)
admin.site.register(Expense)
admin.site.register(UsersDelegations)
admin.site.register(BusinessExpenses)
admin.site.register(Advance)
