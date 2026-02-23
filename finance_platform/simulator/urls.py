from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('signup/', views.signup, name='signup'),

    # İşlemler
    path('transactions/', views.transactions_list, name='transactions'),
    path('transactions/add/', views.add_transaction, name='add_transaction'),
    path('edit/<int:pk>/', views.edit_transaction, name='edit_transaction'),
    path('delete/<int:pk>/', views.delete_transaction, name='delete_transaction'),
    path('mark-paid/<int:pk>/', views.mark_as_paid, name='mark_as_paid'),

    # Raporlar
    path('reports/', views.reports, name='reports'),

    # Bütçe
    path('budgets/', views.budgets_view, name='budgets'),
    path('budgets/delete/<int:pk>/', views.delete_budget, name='delete_budget'),

    # Ayarlar
    path('settings/', views.settings_view, name='settings'),
    path('settings/account/add/', views.add_account, name='add_account'),
    path('settings/account/delete/<int:pk>/', views.delete_account, name='delete_account'),
    path('settings/category/add/', views.add_category, name='add_category'),
    path('settings/category/delete/<int:pk>/', views.delete_category, name='delete_category'),
]
