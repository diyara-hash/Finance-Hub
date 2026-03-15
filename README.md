🚀 Proje Hakkında
Finance Hub, gelir-gider takibi, bütçe planlama ve finansal analiz özellikleri sunan modern bir kişisel finans yönetim platformudur. AI destekli öneriler ve görselleştirilmiş raporlarla paranızı daha bilinçli yönetmenizi sağlar.

✨ Özellikler

📊 Finansal Takip
Gelir & Gider Yönetimi - Kategorilere göre işlem kaydı
Bütçe Planlama - Aylık bütçe hedefleri ve limitler
Fatura Hatırlatıcıları - Ödeme tarihlerini asla kaçırma
Çoklu Hesap Desteği - Banka, nakit, kredi kartı takibi

📈 Analiz & Raporlama
Görsel Dashboard - Gerçek zamanlı finansal durum özeti
Grafikler & İstatistikler - Doughnut, line ve bar grafikleri
Harcama Analizi - Kategori bazlı detaylı raporlar
Trend Analizi - Aylık/yıllık karşılaştırmalar

🤖 AI Özellikleri
Akıllı Kategorizasyon - Otomatik işlem sınıflandırma
Bütçe Önerileri - Kişiselleştirilmiş tasarruf tavsiyeleri
Harcama Tahminleri - Gelecek ay tahmini analizleri

🔐 Güvenlik
JWT Authentication - Güvenli kullanıcı oturumları
Şifreleme - Hassas verilerin korunması
2FA Desteği - İki faktörlü kimlik doğrulama

🛠️ Teknoloji Stack
| Katman             | Teknolojiler                                    |
| ------------------ | ----------------------------------------------- |
| **Frontend**       | React 18, Redux Toolkit, Tailwind CSS, Recharts |
| **Backend**        | Node.js, Express.js, REST API                   |
| **Database**       | MongoDB, Mongoose ODM                           |
| **Authentication** | JWT, bcrypt                                     |
| **AI/ML**          | TensorFlow\.js / OpenAI API                     |
| **Deployment**     | Vercel (Frontend), Render/Railway (Backend)     |

🚀 Kurulum
Gereksinimler
Node.js (v16+)
MongoDB
npm veya yarn

Adım 1: Repo'yu Klonla
git clone https://github.com/diyara-hash/Finance-Hub.git
cd Finance-Hub

Adım 2: Backend Kurulumu
cd backend
npm install

# .env dosyası oluştur
cp .env.example .env

# MongoDB URI ve JWT secret ayarla
# .env içeriği:
# MONGODB_URI=mongodb://localhost:27017/finance-hub
# JWT_SECRET=your-secret-key
# PORT=5000

npm run dev

Adım 3: Frontend Kurulumu
cd ../frontend
npm install
npm start

Uygulama http://localhost:3000 adresinde çalışacaktır.

📱 Ekran Görüntüleri
<p align="center">
  <i>Dashboard, İşlem Ekleme ve Raporlar ekranları yakında eklenecektir...</i>
</p>
🌟 Kullanım
Temel İşlemler
Kayıt Ol → Yeni hesap oluştur
Hesap Ekle → Banka/nakit hesaplarını tanımla
İşlem Kaydet → Gelir/gider ekle
Bütçe Belirle → Kategori limitleri ayarla
Raporları İncele → Finansal analizleri görüntüle

API Endpoints
| Endpoint               | Method   | Açıklama               |
| ---------------------- | -------- | ---------------------- |
| `/api/auth/register`   | POST     | Kullanıcı kaydı        |
| `/api/auth/login`      | POST     | Giriş yap              |
| `/api/transactions`    | GET/POST | İşlemleri listele/ekle |
| `/api/budgets`         | GET/PUT  | Bütçe yönetimi         |
| `/api/reports/summary` | GET      | Özet rapor             |
| `/api/ai/predict`      | POST     | AI tahminleri          |

🗺️ Yol Haritası
[x] Temel CRUD işlemleri
[x] Kimlik doğrulama sistemi
[x] Dashboard ve grafikler
[ ] Mobil uygulama (React Native)
[ ] Banka entegrasyonları
[ ] Gelir-gider tahminleri
[ ] Çoklu dil desteği
[ ] Dark/Light tema

🤝 Katkıda Bulunma
Katkılarınızı bekliyoruz! Lütfen önce bir issue açarak değişiklikleri tartışalım.
Fork yapın
Feature branch oluşturun (git checkout -b feature/amazing-feature)
Commit yapın (git commit -m 'Add amazing feature')
Push yapın (git push origin feature/amazing-feature)
Pull Request açın

👩‍💻 Geliştirici
Diyara Hash
GitHub: @diyara-hash
