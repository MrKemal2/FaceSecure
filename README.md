# FaceSecure - Yüz Tanıma Sistemi

FaceSecure, yüz tanıma teknolojisi kullanarak güvenli kimlik doğrulama sağlayan modern bir web uygulamasıdır. FastAPI backend ve Streamlit frontend ile geliştirilmiş, Docker ile konteynerize edilmiş bir sistemdir.

## 🚀 Özellikler

- **Yüz Tanıma ile Giriş**: Kamera kullanarak yüz tanıma ile güvenli giriş
- **Admin Paneli**: Kullanıcı yönetimi ve sistem kontrolü
- **Çoklu Poz Kayıt**: 10 farklı pozdan yüz verisi toplama
- **Güvenli Şifreleme**: Yüz verilerinin AES şifreleme ile korunması
- **JWT Token Sistemi**: Güvenli oturum yönetimi
- **MongoDB Entegrasyonu**: Hızlı ve güvenilir veri saklama
- **Real-time Kamera**: Anlık yüz yakalama ve doğrulama
- **Docker Desteği**: Kolay kurulum ve dağıtım
- **Başarısız Giriş Loglama**: Güvenlik için detaylı log sistemi

## 🛠️ Teknolojiler

- **Backend**: FastAPI, Python 3.12
- **Frontend**: Streamlit
- **Veritabanı**: MongoDB
- **Yüz Tanıma**: FaceNet, MediaPipe, OpenCV, Numpy
- **Güvenlik**: JWT, Cryptography (Fernet), Bcrypt
- **ML/AI**: TensorFlow, Keras-FaceNet, Scikit-learn
- **Konteynerizasyon**: Docker, Docker Compose
- 

## 📋 Gereksinimler

- Docker ve Docker Compose (Önerilen)
- Python 3.11+ (Manuel kurulum için)
- Webcam/Kamera

## 🔧 Kurulum

### Docker ile Kurulum (Önerilen)

#### 1. Projeyi Klonlayın

```bash
git clone https://github.com/AliKemalSahin/FaceSecure.git
cd FaceSecure
```

#### 2. Docker Compose ile Başlatın

```bash
docker-compose up -d
```

Bu komut otomatik olarak:

- MongoDB konteynerini başlatır
- Backend API'yi derler ve çalıştırır
- Frontend uygulamasını başlatır
- Gerekli ağ bağlantılarını kurar

#### 3. Uygulamaya Erişin

- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Dokümantasyonu**: http://localhost:8000/docs

### Manuel Kurulum

#### 1. Projeyi Klonlayın

```bash
git clone https://github.com/MrKemal2/FaceSecure.git
cd FaceSecure
```

#### 2. MongoDB'yi Başlatın

MongoDB'nin sisteminizde kurulu ve çalışır durumda olduğundan emin olun.

#### 3. Backend Kurulumu

```bash
# Backend bağımlılıklarını yükleyin
pip install -r requirements-backend.txt

# Backend'i başlatın
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

#### 4. Frontend Kurulumu (Yeni Terminal)

```bash
# Frontend bağımlılıklarını yükleyin
pip install -r requirements-frontend.txt

# Frontend'i başlatın
streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0  
```

## 🚀 İlk Kullanım

### Admin Hesabı

Sistem ilk çalıştırıldığında otomatik olarak bir admin hesabı oluşturulur:

- **Kullanıcı Adı**: admin
- **Şifre**: admin

### Yeni Kullanıcı Ekleme

1. Admin hesabı ile giriş yapın
2. "Yeni Kullanıcı Ekle" bölümünde 10 farklı pozdan fotoğraf çekin
3. Kullanıcının ad-soyad ve kullanıcı adı bilgilerini girin
4. Kayıt işlemini tamamlayın

## 📱 Kullanım

### Admin Girişi

1. Streamlit uygulamasında "Admin Girişi" sekmesini seçin
2. Varsayılan admin bilgileri ile giriş yapın (Kullanıcı adı: admin Şifre: admin)
3. Admin panelinde kullanıcı yönetimi yapabilirsiniz

### Yeni Kullanıcı Ekleme

1. Admin panelinde "Yeni Kullanıcı Ekle" bölümüne gidin
2. Kameradan 10 farklı poz çekin (sağa, sola, yukarı, aşağı bakarak)
3. Tüm pozlar tamamlandıktan sonra:
   - Ad Soyad bilgisini girin
   - Kullanıcı adını girin
   - "Yüz Kaydını Tamamla" butonuna tıklayın

### Yüz Tanıma ile Giriş

1. "Kullanıcı Girişi" sekmesinde kameradan fotoğraf çekin
2. Sistem yüzünüzü tanıyacak ve otomatik giriş yapacaktır
3. Başarılı girişte üye paneline yönlendirilirsiniz

### Kullanıcı Yönetimi

- Admin panelinde tüm kullanıcıları görüntüleyebilirsiniz
- Admin olmayan kullanıcıları silebilirsiniz
- Kullanıcı listesinde ad, kullanıcı adı ve yetki bilgileri görünür




