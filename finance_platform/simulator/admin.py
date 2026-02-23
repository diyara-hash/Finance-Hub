from django.contrib import admin
from .models import Category, Transaction, Account, Budget, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'color', 'is_bill', 'parent')
    list_filter = ('is_bill',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'category', 'account', 'amount', 'date', 'is_paid')
    list_filter = ('type', 'is_paid', 'category')
    search_fields = ('description',)


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'account_type', 'balance', 'is_active')
    list_filter = ('account_type', 'is_active')


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'amount', 'month', 'year')
    list_filter = ('month', 'year')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
