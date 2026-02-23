import os
import sys
from datetime import datetime

# Django projesi dışında çalışırken simulator.utils importu sorun olabilir.
# Ancak kullanıcı aynı klasör yapısında çalışmamızı istediği için
# path ayarı yaparak import etmeyi deneyeceğiz.
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from simulator.utils import load_data, save_data, signup, login
except ImportError:
    # Eğer simulator paketi bulunamazsa (standalone çalışma durumu)
    # utils.py dosyasının yanındaysak doğrudan import deneyelim
    try:
        from utils import load_data, save_data, signup, login
    except ImportError:
        print("Hata: Gerekli 'utils.py' fonksiyonları bulunamadı.")
        sys.exit(1)

DATA_FILE = "finance_data.json"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_valid_amount():
    while True:
        try:
            amount = float(input("Tutar: "))
            if amount <= 0:
                print("Tutar pozitif olmalıdır.")
                continue
            return amount
        except ValueError:
            print("Geçerli bir sayı giriniz.")

def get_valid_date():
    while True:
        date_str = input("Tarih (YYYY-MM-DD) [Boş = Bugün]: ").strip()
        if not date_str:
            return datetime.now().strftime("%Y-%m-%d")
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            print("Hatalı format. Lütfen YYYY-MM-DD formatında giriniz.")

def get_non_empty_input(prompt):
    while True:
        val = input(prompt).strip()
        if val:
            return val
        print("Bu alan boş bırakılamaz.")

def show_report(data, username):
    clear_screen()
    print(f"--- FİNANS RAPORU ({username}) ---")
    user_data = [d for d in data if d.get('user') == username]
    
    if not user_data:
        print("Henüz işlem kaydı yok.")
        input("\nDevam etmek için Enter'a basın...")
        return

    print(f"{'Tarih':<12} {'Tür':<10} {'Kategori':<15} {'Açıklama':<20} {'Tutar':>10}")
    print("-" * 70)

    total_income = 0
    total_expense = 0

    for item in user_data:
        amount = item['amount']
        if item['type'] == 'income':
            total_income += amount
        else:
            total_expense += amount
        
        print(f"{item['date']:<12} {item['type']:<10} {item['category']:<15} {item['description']:<20} {amount:>10.2f}")

    print("-" * 70)
    print(f"Toplam Gelir : {total_income:.2f}")
    print(f"Toplam Gider : {total_expense:.2f}")
    print(f"Net Bakiye   : {total_income - total_expense:.2f}")
    
    input("\nDevam etmek için Enter'a basın...")

def add_transaction(data, username, type_):
    clear_screen()
    print(f"--- {type_.upper()} EKLE ---")
    
    amount = get_valid_amount()
    category = get_non_empty_input("Kategori: ")
    description = get_non_empty_input("Açıklama: ")
    date = get_valid_date()

    transaction = {
        "user": username,
        "type": type_,
        "amount": amount,
        "category": category,
        "description": description,
        "date": date
    }
    
    data.append(transaction)
    save_data(data, DATA_FILE)
    print("İşlem kaydedildi.")
    input("\nDevam etmek için Enter'a basın...")

def main_menu(username):
    data = load_data(DATA_FILE)
    
    while True:
        clear_screen()
        print(f"--- Hoşgeldiniz, {username} ---")
        print("1. Gelir Ekle")
        print("2. Gider Ekle")
        print("3. Raporu Göster")
        print("4. Çıkış Yap")
        
        choice = input("Seçiminiz: ")
        
        if choice == '1':
            add_transaction(data, username, 'income')
        elif choice == '2':
            add_transaction(data, username, 'expense')
        elif choice == '3':
            show_report(data, username)
        elif choice == '4':
            break
        else:
            print("Geçersiz seçim.")

def main():
    while True:
        clear_screen()
        print(r"""
==================================================
   ___                             _   _       
  / _ \ _ __   ___ _ __ __ _| |_(_) ___  _ __ 
 | | | | '_ \ / _ \ '__/ _` | __| |/ _ \| '_ \ 
 | |_| | |_) |  __/ | | (_| | |_| | (_) | | | |
  \___/| .__/ \___|_|  \__,_|\__|_|\___/|_| |_|
       |_|                                     
          Fx: INCOME & EXPENSE TRACKER
==================================================
        """)
        print("1. Giriş Yap (Login)")
        print("2. Kayıt Ol (Signup)")
        print("3. Çıkış (Exit)")
        print("-" * 50)
        
        choice = input("Seçiminiz: ")
        
        if choice == '1':
            username = input("Kullanıcı Adı: ")
            password = input("Şifre: ")
            success, msg = login(username, password)
            print(msg)
            if success:
                input("Devam etmek için Enter...")
                main_menu(username)
            else:
                input("Devam etmek için Enter...")
                
        elif choice == '2':
            username = input("Kullanıcı Adı: ")
            password = input("Şifre: ")
            success, msg = signup(username, password)
            print(msg)
            input("Devam etmek için Enter...")
            
        elif choice == '3':
            print("Güle güle...")
            break
        else:
            print("Geçersiz seçim.")

if __name__ == "__main__":
    main()
