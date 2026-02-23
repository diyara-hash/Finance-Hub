from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    """Banka hesabı, kredi kartı, nakit cüzdan veya yatırım hesabı."""
    TYPE_CHOICES = (
        ('bank', 'Banka Hesabı'),
        ('credit_card', 'Kredi Kartı'),
        ('cash', 'Nakit'),
        ('investment', 'Yatırım'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    name = models.CharField(max_length=100, verbose_name="Hesap Adı")
    account_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='cash', verbose_name="Hesap Türü")
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Bakiye")
    color = models.CharField(max_length=7, default='#6366f1', verbose_name="Renk")
    icon = models.CharField(max_length=50, default='bi-wallet2', verbose_name="İkon")
    credit_limit = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name="Kredi Limiti")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.get_account_type_display()})"

    @property
    def usage_percent(self):
        if self.account_type == 'credit_card' and self.credit_limit:
            return min(round((abs(self.balance) / self.credit_limit) * 100), 100)
        return 0

    class Meta:
        verbose_name = "Hesap"
        verbose_name_plural = "Hesaplar"
        ordering = ['name']


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="Kategori Adı")
    icon = models.CharField(max_length=50, default="bi-tag-fill", verbose_name="İkon")
    color = models.CharField(max_length=50, default="#6366f1", verbose_name="Renk")
    is_bill = models.BooleanField(default=False, verbose_name="Fatura mı?")
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='subcategories', verbose_name="Üst Kategori")

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} → {self.name}"
        return self.name

    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"
        ordering = ['name']


class Tag(models.Model):
    """İşlem etiketleri."""
    name = models.CharField(max_length=30, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tags')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Etiket"
        verbose_name_plural = "Etiketler"


class Transaction(models.Model):
    TYPE_CHOICES = (
        ('income', 'Gelir'),
        ('expense', 'Gider'),
        ('transfer', 'Transfer'),
    )

    RECURRING_CHOICES = (
        ('none', 'Tekrar Yok'),
        ('daily', 'Günlük'),
        ('weekly', 'Haftalık'),
        ('monthly', 'Aylık'),
        ('yearly', 'Yıllık'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name="Tür")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Kategori")
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='transactions', verbose_name="Hesap")
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Tutar")
    description = models.CharField(max_length=255, blank=True, verbose_name="Açıklama")
    tags = models.ManyToManyField(Tag, blank=True, related_name='transactions', verbose_name="Etiketler")
    date = models.DateField(auto_now_add=True, verbose_name="Tarih")

    # Bill specific
    due_date = models.DateField(null=True, blank=True, verbose_name="Son Ödeme Tarihi")
    is_paid = models.BooleanField(default=False, verbose_name="Ödendi mi?")

    # Recurring
    is_recurring = models.BooleanField(default=False, verbose_name="Tekrarlayan mı?")
    recurring_period = models.CharField(max_length=10, choices=RECURRING_CHOICES, default='none',
                                        verbose_name="Tekrar Periyodu")

    class TransactionQuerySet(models.QuerySet):
        def expenses(self):
            return self.filter(type='expense')

        def incomes(self):
            return self.filter(type='income')

        def paid(self):
            return self.filter(is_paid=True)

        def unpaid(self):
            return self.filter(is_paid=False)

    objects = TransactionQuerySet.as_manager()

    def __str__(self):
        return f"{self.get_type_display()} - {self.amount}₺"

    @property
    def is_overdue(self):
        from datetime import date
        if self.category and self.category.is_bill and not self.is_paid and self.due_date and self.due_date < date.today():
            return True
        return False

    def clean(self):
        from django.core.exceptions import ValidationError
        super().clean()
        if self.category and self.category.is_bill:
            if not self.due_date:
                raise ValidationError({'due_date': 'Bu kategori (Fatura) için son ödeme tarihi zorunludur.'})

    class Meta:
        verbose_name = "İşlem"
        verbose_name_plural = "İşlemler"
        ordering = ['-date', '-id']


class Budget(models.Model):
    """Kategori bazlı aylık bütçe."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Kategori")
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Bütçe Limiti")
    month = models.IntegerField(verbose_name="Ay")  # 1-12
    year = models.IntegerField(verbose_name="Yıl")

    @property
    def spent(self):
        return Transaction.objects.filter(
            user=self.user,
            category=self.category,
            type='expense',
            date__month=self.month,
            date__year=self.year,
        ).aggregate(total=models.Sum('amount'))['total'] or 0

    @property
    def remaining(self):
        return self.amount - self.spent

    @property
    def percent_used(self):
        if self.amount > 0:
            return min(round((self.spent / self.amount) * 100), 100)
        return 0

    @property
    def is_over_budget(self):
        return self.spent >= self.amount

    @property
    def is_warning(self):
        return self.percent_used >= 80 and not self.is_over_budget

    def __str__(self):
        return f"{self.category.name} - {self.month}/{self.year}"

    class Meta:
        verbose_name = "Bütçe"
        verbose_name_plural = "Bütçeler"
        unique_together = ['user', 'category', 'month', 'year']
