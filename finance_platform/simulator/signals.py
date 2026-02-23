from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


@receiver(post_migrate)
def create_default_categories(sender, **kwargs):
    if sender.name != 'simulator':
        return

    from .models import Category

    categories = [
        # Fatura Kategorileri (is_bill=True)
        {'name': 'Elektrik',  'icon': 'bi-lightning-fill',   'color': '#f59e0b', 'is_bill': True},
        {'name': 'Su',        'icon': 'bi-droplet-fill',     'color': '#3b82f6', 'is_bill': True},
        {'name': 'Doğalgaz',  'icon': 'bi-fire',             'color': '#ef4444', 'is_bill': True},
        {'name': 'İnternet',  'icon': 'bi-wifi',             'color': '#06b6d4', 'is_bill': True},
        {'name': 'Telefon',   'icon': 'bi-phone-fill',       'color': '#8b5cf6', 'is_bill': True},
        # Normal Gider Kategorileri
        {'name': 'Market',    'icon': 'bi-cart-fill',         'color': '#10b981', 'is_bill': False},
        {'name': 'Ulaşım',   'icon': 'bi-bus-front-fill',    'color': '#f97316', 'is_bill': False},
        {'name': 'Kira',      'icon': 'bi-house-door-fill',   'color': '#ec4899', 'is_bill': False},
        {'name': 'Eğlence',  'icon': 'bi-controller',        'color': '#a855f7', 'is_bill': False},
        {'name': 'Yemek',    'icon': 'bi-cup-hot-fill',      'color': '#f43f5e', 'is_bill': False},
        {'name': 'Sağlık',   'icon': 'bi-heart-pulse-fill',  'color': '#14b8a6', 'is_bill': False},
        {'name': 'Eğitim',   'icon': 'bi-book-fill',         'color': '#6366f1', 'is_bill': False},
        {'name': 'Giyim',    'icon': 'bi-bag-fill',          'color': '#d946ef', 'is_bill': False},
        {'name': 'Diğer',    'icon': 'bi-three-dots',        'color': '#64748b', 'is_bill': False},
    ]

    for cat_data in categories:
        Category.objects.get_or_create(name=cat_data['name'], defaults=cat_data)


@receiver(post_save, sender=User)
def create_default_account(sender, instance, created, **kwargs):
    """Yeni kullanıcı oluşturulduğunda varsayılan Nakit hesabı ekle."""
    if created:
        from .models import Account
        Account.objects.get_or_create(
            user=instance,
            name='Nakit Cüzdan',
            defaults={
                'account_type': 'cash',
                'balance': 0,
                'color': '#10b981',
                'icon': 'bi-wallet2',
            }
        )
