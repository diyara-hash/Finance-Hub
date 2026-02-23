import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finance_platform.settings')
django.setup()

from simulator.models import Category

categories = [
    # Bill Categories (is_bill=True)
    {'name': 'Elektrik', 'icon': 'bi-lightning-fill', 'color': 'bg-warning', 'is_bill': True},
    {'name': 'Doğalgaz', 'icon': 'bi-fire', 'color': 'bg-secondary', 'is_bill': True},
    {'name': 'Su', 'icon': 'bi-water', 'color': 'bg-primary', 'is_bill': True},
    {'name': 'İnternet', 'icon': 'bi-wifi', 'color': 'bg-info', 'is_bill': True},
    {'name': 'Telefon', 'icon': 'bi-phone', 'color': 'bg-dark', 'is_bill': True},
    {'name': 'Kira', 'icon': 'bi-house-door-fill', 'color': 'bg-danger', 'is_bill': True},
    
    # Expense Categories (is_bill=False)
    {'name': 'Market', 'icon': 'bi-cart-fill', 'color': 'bg-success', 'is_bill': False},
    {'name': 'Yakıt', 'icon': 'bi-fuel-pump-fill', 'color': 'bg-warning', 'is_bill': False},
    {'name': 'Eğitim', 'icon': 'bi-book-fill', 'color': 'bg-info', 'is_bill': False},
    {'name': 'Diğer', 'icon': 'bi-three-dots', 'color': 'bg-secondary', 'is_bill': False},
]

for cat_data in categories:
    Category.objects.get_or_create(name=cat_data['name'], defaults=cat_data)
    print(f"Created/Updated Category: {cat_data['name']}")

print("Categories populated successfully!")
