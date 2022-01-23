from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('deleg/login/', views.login_view, name='login_view'),

    path('deleg/logout/', views.logout_view, name='logout_view'),

    path('deleg/', views.delegations, name='delegations'),

    path('deleg/add_delegation/', views.add_delegation, name='add_delegation'),

    path('deleg/<int:delegation_id>/', views.delegation, name='delegation'),

    path('deleg/<int:delegation_id>/add_users/', views.add_users, name='add_users'),

    path('deleg/<int:delegation_id>/add_expense/', views.add_expense, name='add_expense'),
]
