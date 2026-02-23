from django import forms
from .models import Transaction, Account, Budget, Category


class TransactionForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'fh-select', 'id': 'id_category'}),
        required=False,
        label="Kategori"
    )
    account = forms.ModelChoiceField(
        queryset=Account.objects.none(),
        widget=forms.Select(attrs={'class': 'fh-select', 'id': 'id_account'}),
        required=False,
        label="Hesap"
    )

    class Meta:
        model = Transaction
        fields = ['type', 'category', 'account', 'amount', 'description', 'due_date', 'is_paid',
                  'is_recurring', 'recurring_period']
        widgets = {
            'type': forms.Select(attrs={'class': 'fh-select', 'id': 'id_type'}),
            'amount': forms.NumberInput(attrs={'class': 'fh-input', 'step': '0.01', 'placeholder': '0.00'}),
            'description': forms.TextInput(attrs={'class': 'fh-input', 'placeholder': 'Açıklama girin...'}),
            'due_date': forms.DateInput(attrs={'class': 'fh-input', 'type': 'date', 'id': 'id_due_date'}),
            'is_paid': forms.CheckboxInput(attrs={'class': 'fh-checkbox', 'id': 'id_is_paid'}),
            'is_recurring': forms.CheckboxInput(attrs={'class': 'fh-checkbox', 'id': 'id_is_recurring'}),
            'recurring_period': forms.Select(attrs={'class': 'fh-select', 'id': 'id_recurring_period'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['account'].queryset = Account.objects.filter(user=user, is_active=True)

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        due_date = cleaned_data.get('due_date')
        if category and category.is_bill:
            if not due_date:
                self.add_error('due_date', 'Bu kategori için son ödeme tarihi zorunludur.')
        return cleaned_data


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'account_type', 'balance', 'color', 'icon', 'credit_limit']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'fh-input', 'placeholder': 'Hesap adı'}),
            'account_type': forms.Select(attrs={'class': 'fh-select'}),
            'balance': forms.NumberInput(attrs={'class': 'fh-input', 'step': '0.01'}),
            'color': forms.TextInput(attrs={'class': 'fh-input', 'type': 'color'}),
            'icon': forms.TextInput(attrs={'class': 'fh-input', 'placeholder': 'bi-wallet2'}),
            'credit_limit': forms.NumberInput(attrs={'class': 'fh-input', 'step': '0.01'}),
        }


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'amount', 'month', 'year']
        widgets = {
            'category': forms.Select(attrs={'class': 'fh-select'}),
            'amount': forms.NumberInput(attrs={'class': 'fh-input', 'step': '0.01', 'placeholder': 'Limit'}),
            'month': forms.Select(attrs={'class': 'fh-select'}, choices=[
                (i, m) for i, m in enumerate(
                    ['', 'Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran',
                     'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık'], 0
                ) if i > 0
            ]),
            'year': forms.NumberInput(attrs={'class': 'fh-input', 'placeholder': '2026'}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'icon', 'color', 'is_bill', 'parent']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'fh-input', 'placeholder': 'Kategori adı'}),
            'icon': forms.TextInput(attrs={'class': 'fh-input', 'placeholder': 'bi-tag-fill'}),
            'color': forms.TextInput(attrs={'class': 'fh-input', 'type': 'color'}),
            'is_bill': forms.CheckboxInput(attrs={'class': 'fh-checkbox'}),
            'parent': forms.Select(attrs={'class': 'fh-select'}),
        }
