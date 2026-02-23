from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Q, Count
from django.db.models.functions import TruncMonth, ExtractMonth, ExtractYear
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.core.paginator import Paginator
from collections import defaultdict
from datetime import date, timedelta, datetime
from decimal import Decimal
import json

from .models import Transaction, Category, Account, Budget, Tag
from .forms import TransactionForm, AccountForm, BudgetForm, CategoryForm


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def dashboard(request):
    if request.method == "POST":
        form = TransactionForm(request.POST, user=request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('dashboard')
    else:
        form = TransactionForm(user=request.user)

    today = date.today()
    transactions = Transaction.objects.filter(user=request.user).order_by('-date', '-id')

    # Finansal Özet
    total_income = transactions.incomes().aggregate(s=Sum('amount'))['s'] or Decimal('0')
    total_expense = transactions.expenses().aggregate(s=Sum('amount'))['s'] or Decimal('0')
    balance = total_income - total_expense

    # Son 10 işlem
    recent_transactions = transactions[:10]

    # Hesaplar
    accounts = Account.objects.filter(user=request.user, is_active=True)

    # Bu ay
    month_start = today.replace(day=1)
    month_income = transactions.incomes().filter(date__gte=month_start).aggregate(s=Sum('amount'))['s'] or Decimal('0')
    month_expense = transactions.expenses().filter(date__gte=month_start).aggregate(s=Sum('amount'))['s'] or Decimal('0')

    # Geçen ay
    last_month_end = month_start - timedelta(days=1)
    last_month_start = last_month_end.replace(day=1)
    last_month_expense = transactions.expenses().filter(
        date__gte=last_month_start, date__lte=last_month_end
    ).aggregate(s=Sum('amount'))['s'] or Decimal('0')

    # Harcama trendi (artış/azalış yüzdesi)
    if last_month_expense > 0:
        expense_trend = round(((month_expense - last_month_expense) / last_month_expense) * 100, 1)
    else:
        expense_trend = 0

    # Kategori dağılımı (bu ay)
    category_data = transactions.expenses().filter(date__gte=month_start).values(
        'category__name', 'category__color', 'category__icon'
    ).annotate(total=Sum('amount')).order_by('-total')[:8]

    category_labels = [c['category__name'] or 'Diğer' for c in category_data]
    category_amounts = [float(c['total']) for c in category_data]
    category_colors = [c['category__color'] or '#64748b' for c in category_data]

    # Son 7 gün nakit akışı
    seven_days_ago = today - timedelta(days=6)
    daily_data = []
    for i in range(7):
        d = seven_days_ago + timedelta(days=i)
        inc = transactions.incomes().filter(date=d).aggregate(s=Sum('amount'))['s'] or 0
        exp = transactions.expenses().filter(date=d).aggregate(s=Sum('amount'))['s'] or 0
        daily_data.append({
            'date': d.strftime('%d %b'),
            'income': float(inc),
            'expense': float(exp),
            'net': float(inc) - float(exp),
        })

    daily_labels = json.dumps([d['date'] for d in daily_data])
    daily_income_data = json.dumps([d['income'] for d in daily_data])
    daily_expense_data = json.dumps([d['expense'] for d in daily_data])

    # Aylık trend (son 6 ay)
    monthly_data = []
    for i in range(5, -1, -1):
        m_date = today - timedelta(days=i * 30)
        m_start = m_date.replace(day=1)
        if m_date.month == 12:
            m_end = m_date.replace(year=m_date.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            m_end = m_date.replace(month=m_date.month + 1, day=1) - timedelta(days=1)
        m_inc = transactions.incomes().filter(date__gte=m_start, date__lte=m_end).aggregate(s=Sum('amount'))['s'] or 0
        m_exp = transactions.expenses().filter(date__gte=m_start, date__lte=m_end).aggregate(s=Sum('amount'))['s'] or 0
        monthly_data.append({
            'label': m_start.strftime('%b %Y'),
            'income': float(m_inc),
            'expense': float(m_exp),
        })

    monthly_labels = json.dumps([m['label'] for m in monthly_data])
    monthly_income_data = json.dumps([m['income'] for m in monthly_data])
    monthly_expense_data = json.dumps([m['expense'] for m in monthly_data])

    # Bütçeler (bu ay)
    budgets = Budget.objects.filter(user=request.user, month=today.month, year=today.year)

    # Fatura widget
    three_days_later = today + timedelta(days=3)
    all_expenses = Transaction.objects.filter(user=request.user, type='expense')
    overdue_bills = all_expenses.filter(category__is_bill=True, is_paid=False, due_date__lt=today)
    upcoming_bills = all_expenses.filter(category__is_bill=True, is_paid=False, due_date__gte=today, due_date__lte=three_days_later)
    total_unpaid_bills = all_expenses.filter(category__is_bill=True, is_paid=False).aggregate(s=Sum('amount'))['s'] or 0

    bill_category_ids = list(Category.objects.filter(is_bill=True).values_list('id', flat=True))

    context = {
        'form': form,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'month_income': month_income,
        'month_expense': month_expense,
        'expense_trend': expense_trend,
        'recent_transactions': recent_transactions,
        'accounts': accounts,
        'budgets': budgets,
        # Charts
        'category_labels': json.dumps(category_labels),
        'category_amounts': json.dumps(category_amounts),
        'category_colors': json.dumps(category_colors),
        'daily_labels': daily_labels,
        'daily_income_data': daily_income_data,
        'daily_expense_data': daily_expense_data,
        'monthly_labels': monthly_labels,
        'monthly_income_data': monthly_income_data,
        'monthly_expense_data': monthly_expense_data,
        # Bills
        'overdue_bills': overdue_bills,
        'upcoming_bills': upcoming_bills,
        'total_unpaid_bills': total_unpaid_bills,
        'bill_category_ids': bill_category_ids,
        'today': today,
    }
    return render(request, "simulator/dashboard.html", context)


@login_required
def transactions_list(request):
    transactions = Transaction.objects.filter(user=request.user)

    # Filtreleme
    tx_type = request.GET.get('type', '')
    category_id = request.GET.get('category', '')
    account_id = request.GET.get('account', '')
    search = request.GET.get('search', '')
    date_preset = request.GET.get('preset', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    today = date.today()

    if date_preset == 'today':
        transactions = transactions.filter(date=today)
    elif date_preset == 'week':
        transactions = transactions.filter(date__gte=today - timedelta(days=today.weekday()))
    elif date_preset == 'month':
        transactions = transactions.filter(date__month=today.month, date__year=today.year)
    elif start_date and end_date:
        transactions = transactions.filter(date__range=[start_date, end_date])

    if tx_type:
        transactions = transactions.filter(type=tx_type)
    if category_id:
        transactions = transactions.filter(category_id=category_id)
    if account_id:
        transactions = transactions.filter(account_id=account_id)
    if search:
        transactions = transactions.filter(
            Q(description__icontains=search) | Q(category__name__icontains=search)
        )

    # Toplam
    total = transactions.aggregate(
        income=Sum('amount', filter=Q(type='income')),
        expense=Sum('amount', filter=Q(type='expense')),
    )
    total_income = total['income'] or 0
    total_expense = total['expense'] or 0

    # Sayfalama
    paginator = Paginator(transactions, 20)
    page = request.GET.get('page', 1)
    transactions_page = paginator.get_page(page)

    categories = Category.objects.all()
    accounts = Account.objects.filter(user=request.user, is_active=True)
    form = TransactionForm(user=request.user)
    bill_category_ids = list(Category.objects.filter(is_bill=True).values_list('id', flat=True))

    return render(request, 'simulator/transactions.html', {
        'transactions': transactions_page,
        'categories': categories,
        'accounts': accounts,
        'form': form,
        'bill_category_ids': bill_category_ids,
        'total_income': total_income,
        'total_expense': total_expense,
        # Preserve filters
        'current_type': tx_type,
        'current_category': category_id,
        'current_account': account_id,
        'current_search': search,
        'current_preset': date_preset,
    })


@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST, user=request.user)
        if form.is_valid():
            t = form.save(commit=False)
            t.user = request.user
            t.save()
            next_url = request.POST.get('next', 'dashboard')
            return redirect(next_url)
    return redirect('dashboard')


@login_required
def mark_as_paid(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        transaction.is_paid = True
        transaction.save()
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))


@login_required
def edit_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction, user=request.user)
        if form.is_valid():
            form.save()
            return redirect(request.POST.get('next', 'dashboard'))
    else:
        form = TransactionForm(instance=transaction, user=request.user)

    bill_category_ids = list(Category.objects.filter(is_bill=True).values_list('id', flat=True))
    return render(request, 'simulator/edit_transaction.html', {
        'form': form,
        'transaction': transaction,
        'bill_category_ids': bill_category_ids,
    })


@login_required
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        transaction.delete()
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))


@login_required
def reports(request):
    today = date.today()
    transactions = Transaction.objects.filter(user=request.user)

    # Aylık trend (son 12 ay)
    monthly_trend = []
    for i in range(11, -1, -1):
        d = today - timedelta(days=i * 30)
        m_start = d.replace(day=1)
        if d.month == 12:
            m_end = d.replace(year=d.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            m_end = d.replace(month=d.month + 1, day=1) - timedelta(days=1)
        inc = transactions.incomes().filter(date__gte=m_start, date__lte=m_end).aggregate(s=Sum('amount'))['s'] or 0
        exp = transactions.expenses().filter(date__gte=m_start, date__lte=m_end).aggregate(s=Sum('amount'))['s'] or 0
        monthly_trend.append({
            'label': m_start.strftime('%b %y'),
            'income': float(inc),
            'expense': float(exp),
        })

    # Kategori analizi (tüm zamanlar)
    cat_analysis = transactions.expenses().values(
        'category__name', 'category__color', 'category__icon'
    ).annotate(total=Sum('amount'), count=Count('id')).order_by('-total')

    # Bu ay vs geçen ay
    month_start = today.replace(day=1)
    this_month_exp = transactions.expenses().filter(date__gte=month_start).aggregate(s=Sum('amount'))['s'] or 0
    last_month_end = month_start - timedelta(days=1)
    last_month_start = last_month_end.replace(day=1)
    last_month_exp = transactions.expenses().filter(
        date__gte=last_month_start, date__lte=last_month_end
    ).aggregate(s=Sum('amount'))['s'] or 0

    context = {
        'monthly_labels': json.dumps([m['label'] for m in monthly_trend]),
        'monthly_income': json.dumps([m['income'] for m in monthly_trend]),
        'monthly_expense': json.dumps([m['expense'] for m in monthly_trend]),
        'cat_analysis': cat_analysis,
        'cat_labels': json.dumps([c['category__name'] or 'Diğer' for c in cat_analysis]),
        'cat_amounts': json.dumps([float(c['total']) for c in cat_analysis]),
        'cat_colors': json.dumps([c['category__color'] or '#64748b' for c in cat_analysis]),
        'this_month_exp': this_month_exp,
        'last_month_exp': last_month_exp,
    }
    return render(request, 'simulator/reports.html', context)


@login_required
def budgets_view(request):
    today = date.today()

    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            return redirect('budgets')
    else:
        form = BudgetForm(initial={'month': today.month, 'year': today.year})

    budgets = Budget.objects.filter(user=request.user, month=today.month, year=today.year)

    # Toplam bütçe ve toplam harcama
    total_budget = budgets.aggregate(s=Sum('amount'))['s'] or 0
    total_spent = sum(b.spent for b in budgets)

    return render(request, 'simulator/budgets.html', {
        'form': form,
        'budgets': budgets,
        'total_budget': total_budget,
        'total_spent': total_spent,
        'today': today,
    })


@login_required
def delete_budget(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    if request.method == 'POST':
        budget.delete()
    return redirect('budgets')


@login_required
def settings_view(request):
    accounts = Account.objects.filter(user=request.user)
    categories = Category.objects.filter(parent=None)
    account_form = AccountForm()
    category_form = CategoryForm()

    return render(request, 'simulator/settings.html', {
        'accounts': accounts,
        'categories': categories,
        'account_form': account_form,
        'category_form': category_form,
    })


@login_required
def add_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            acc = form.save(commit=False)
            acc.user = request.user
            acc.save()
    return redirect('settings')


@login_required
def delete_account(request, pk):
    account = get_object_or_404(Account, pk=pk, user=request.user)
    if request.method == 'POST':
        account.delete()
    return redirect('settings')


@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('settings')


@login_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
    return redirect('settings')
