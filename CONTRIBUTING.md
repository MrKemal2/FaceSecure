# Katkıda Bulunma Rehberi

FaceSecure projesine katkıda bulunmak istediğiniz için teşekkür ederiz! Aşağıda, projeye katkıda bulunmak için izlemeniz gereken adımları bulabilirsiniz.

## Geliştirme Ortamı Kurulumu

1. Projeyi forklayın ve klonlayın:
```bash
git clone https://github.com/[kullanıcı-adınız]/FaceSecure.git
cd FaceSecure
```

2. Sanal ortam oluşturun ve bağımlılıkları yükleyin:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
pip install -r requirements.txt
```

3. Ortam değişkenlerini ayarlayın:
```bash
cp .env .env
# .env dosyasını düzenleyin
```

## Geliştirme Süreci

1. Yeni bir branch oluşturun:
```bash
git checkout -b feature/yeni-ozellik
```

2. Değişikliklerinizi yapın ve commit edin:
```bash
git add .
git commit -m "Yeni özellik: Açıklama"
```

3. Branch'inizi push edin:
```bash
git push origin feature/yeni-ozellik
```

4. GitHub üzerinden Pull Request oluşturun.

## Kod Standartları

- PEP 8 standartlarına uygun kod yazın
- Fonksiyonlar ve sınıflar için docstring ekleyin
- Karmaşık kod bloklarını açıklayan yorumlar ekleyin
- Değişken ve fonksiyon isimlerini anlamlı ve Türkçe karakterler içermeyecek şekilde seçin

## Test

- Yeni özellikler için testler ekleyin
- Mevcut testlerin başarılı olduğundan emin olun

## Pull Request Süreci

1. PR açıklamasında değişikliklerinizi detaylı bir şekilde açıklayın
2. Değişikliklerinizin neden gerekli olduğunu belirtin
3. Ekran görüntüleri veya GIF'ler ekleyin (UI değişiklikleri için)

## İletişim

Sorularınız veya önerileriniz için GitHub Issues kullanabilirsiniz.