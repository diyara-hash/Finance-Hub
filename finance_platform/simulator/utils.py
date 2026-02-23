def run_simulation(income, expense, savings, months, inflation):
    results = []
    balance = savings

    for month in range(1, months + 1):
        expense = expense * (1 + inflation)
        monthly_net = income - expense
        balance += monthly_net

        results.append({
            "month": month,
            "expense": round(expense, 2),
            "net": round(monthly_net, 2),
            "balance": round(balance, 2)
        })

    return results

def filter_by_date(start_date, end_date):
    """
    Returns (incomes, expenses) filtered by start_date and end_date (inclusive).
    """
    from .models import Transaction
    
    transactions = Transaction.objects.filter(date__range=[start_date, end_date])
    
    incomes = transactions.filter(type='income')
    expenses = transactions.filter(type='expense')
    
    return incomes, expenses

import json
import os
import hashlib

def load_data(filename="tracker_data.json"):
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_data(data, filename="tracker_data.json"):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def load_users(filename="users.json"):
    if not os.path.exists(filename):
        return {}
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}

def save_users(users, filename="users.json"):
    with open(filename, 'w') as f:
        json.dump(users, f, indent=4)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def signup(username, password, filename="users.json"):
    users = load_users(filename)
    if username in users:
        return False, "Kullanıcı adı zaten var."
    
    users[username] = hash_password(password)
    save_users(users, filename)
    return True, "Kayıt başarılı."

def login(username, password, filename="users.json"):
    users = load_users(filename)
    if username not in users:
        return False, "Kullanıcı bulunamadı."
    
    if users[username] == hash_password(password):
        return True, "Giriş başarılı."
    
    return False, "Hatalı şifre."
