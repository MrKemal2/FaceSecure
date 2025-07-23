# FaceSecure - Yüz Tanıma Sistemi

FaceSecure, yüz tanıma teknolojisi kullanarak güvenli kimlik doğrulama sağlayan modern bir web uygulamasıdır. FastAPI backend ve Streamlit frontend ile geliştirilmiştir.

## 🚀 Özellikler

- **Yüz Tanıma ile Giriş**: Kamera kullanarak yüz tanıma ile güvenli giriş
- **Admin Paneli**: Kullanıcı yönetimi ve sistem kontrolü
- **Güvenli Şifreleme**: Yüz verilerinin şifreli saklanması
- **JWT Token Sistemi**: Güvenli oturum yönetimi
- **MongoDB Entegrasyonu**: Hızlı ve güvenilir veri saklama
- **Real-time Kamera**: Anlık yüz yakalama ve doğrulama

## 🛠️ Teknolojiler

- **Backend**: FastAPI, Python
- **Frontend**: Streamlit
- **Veritabanı**: MongoDB
- **Yüz Tanıma**: DeepFace, MediaPipe, OpenCV
- **Güvenlik**: JWT, Cryptography, Bcrypt
- **Diğer**: NumPy, Pandas

## 📋 Gereksinimler

- Python 3.8+
- MongoDB
- Webcam/Kamera

## 🔧 Kurulum

### 1. Projeyi Klonlayın
```bash
git clone https://github.com/AliKemalSahin/FaceSecure.git
cd FaceSecure
```

### 2. Sanal Ortam Oluşturun
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Bağımlılıkları Yükleyin
```bash
pip install -r requirements.txt
```

### 4. MongoDB'yi Başlatın
MongoDB'nin sisteminizde kurulu ve çalışır durumda olduğundan emin olun.

### 5. Ortam Değişkenlerini Ayarlayın
`.env.example` dosyasını `.env` olarak kopyalayın ve gerekli değerleri düzenleyin:
```bash
cp .env.example .env
```

### 6. İlk Admin Kullanıcısını Oluşturun
MongoDB'de admin koleksiyonuna ilk admin kullanıcısını manuel olarak ekleyin:
```javascript
use denemeFaceSecure
db.admin_collection.insertOne({
  "username": "admin",
  "password": "admin123",
  "full_name": "System Administrator",
  "is_admin": true
})
```

## 🚀 Çalıştırma

### Backend'i Başlatın
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### Frontend'i Başlatın (Yeni Terminal)
```bash
streamlit run streamlit_app.py
```

Uygulama şu adreslerde çalışacaktır:
- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Dokümantasyonu**: http://localhost:8000/docs

## 📱 Kullanım

### Admin Girişi
1. Streamlit uygulamasında "Admin Girişi" sekmesini seçin
2. Admin kullanıcı adı ve şifrenizi girin
3. Admin panelinde yeni kullanıcılar ekleyebilirsiniz

### Yeni Kullanıcı Ekleme
1. Admin panelinde kameradan 10 farklı poz çekin
2. Kullanıcının ad-soyad ve kullanıcı adı bilgilerini girin
3. Kayıt işlemini tamamlayın

### Yüz Tanıma ile Giriş
1. "Kullanıcı Girişi" sekmesinde kameradan fotoğraf çekin
2. Sistem yüzünüzü tanıyacak ve otomatik giriş yapacaktır

## 🔒 Güvenlik

- Tüm yüz verileri AES şifreleme ile korunur
- JWT token'lar ile güvenli oturum yönetimi
- Başarısız giriş denemeleri loglanır
- Admin yetkilendirme sistemi

## 📁 Proje Yapısı

```
facesecure/
├── main.py                 # FastAPI ana uygulama
├── streamlit_app.py        # Streamlit frontend
├── database.py             # MongoDB bağlantı ve işlemleri
├── security.py             # Güvenlik ve şifreleme
├── face_detection.py       # Yüz tanıma algoritmaları
├── schemas.py              # Pydantic modelleri
├── routers/
│   ├── users.py           # Kullanıcı API endpoint'leri
│   └── admin.py           # Admin API endpoint'leri
├── requirements.txt        # Python bağımlılıkları
├── .env                   # Ortam değişkenleri
├── .env.example           # Ortam değişkenleri örneği
└── README.md              # Bu dosya
```

## 🔧 Konfigürasyon

### Yüz Tanıma Ayarları
- `SIMILARITY_THRESHOLD`: Yüz eşleştirme hassasiyeti (0.0-1.0)
- `MODEL_NAME`: Kullanılacak yüz tanıma modeli
- `NUM_PICS_TO_ENROLL`: Kayıt için gerekli fotoğraf sayısı

### Güvenlik Ayarları
- `SECRET_KEY`: JWT token şifreleme anahtarı
- `ENCRYPTION_KEY`: Yüz verisi şifreleme anahtarı
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token geçerlilik süresi

## 🐛 Sorun Giderme

### Kamera Erişim Sorunu
- Tarayıcınızın kamera erişim izni verdiğinden emin olun
- HTTPS bağlantısı gerekebilir (production ortamında)

### MongoDB Bağlantı Sorunu
- MongoDB servisinin çalıştığından emin olun
- Bağlantı URL'sini kontrol edin

### Yüz Tanıma Sorunu
- İyi aydınlatma koşullarında fotoğraf çekin
- Yüzünüzün tam görünür olduğundan emin olun
- Similarity threshold değerini ayarlayın

## 🤝 Katkıda Bulunma

1. Bu projeyi fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakın.

## 📞 İletişim

Proje Sahibi - [GitHub](https://github.com/AliKemalSahin)

Proje Linki: [https://github.com/AliKemalSahin/FaceSecure](https://github.com/AliKemalSahin/FaceSecure)

## 🙏 Teşekkürler

- [DeepFace](https://github.com/serengil/deepface) - Yüz tanıma kütüphanesi
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [Streamlit](https://streamlit.io/) - Web app framework
- [MediaPipe](https://mediapipe.dev/) - Yüz algılama