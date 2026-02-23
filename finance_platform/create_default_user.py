import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finance_platform.settings')
django.setup()

from django.contrib.auth.models import User

if not User.objects.filter(id=1).exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print("Superuser 'admin' created with ID 1.")
else:
    print("User with ID 1 already exists.")
