# Bulut Deployment Rehberi

Bu uygulama Streamlit Cloud ve diğer bulut platformlarında çalışacak şekilde optimize edilmiştir.

## Özellikler

- ✅ Google Sheets entegrasyonu (kalıcı veri depolama)
- ✅ Yerel dosya yolu bağımlılığı yok
- ✅ Streamlit Secrets desteği
- ✅ Environment variables desteği
- ✅ Geçici dosya sistemi kullanımı (fallback)

## Streamlit Cloud Deployment

### 1. GitHub Repository Hazırlama

1. Kodunuzu GitHub'a push edin
2. Repository'nin public veya private olduğundan emin olun

### 2. Streamlit Cloud'a Deploy Etme

1. [Streamlit Cloud](https://share.streamlit.io/)'a gidin
2. **New app** butonuna tıklayın
3. GitHub repository'nizi seçin
4. Branch ve main file'ı seçin (`app.py`)
5. **Deploy** butonuna tıklayın

### 3. Secrets Yapılandırması

1. Streamlit Cloud'da uygulamanızın sayfasına gidin
2. **Settings** > **Secrets**'e tıklayın
3. `.streamlit/secrets.toml.example` dosyasındaki formatı kullanarak secrets ekleyin:

```toml
USE_GOOGLE_SHEETS = "true"
GOOGLE_SHEET_ID = "your_sheet_id_here"
GOOGLE_CREDENTIALS_JSON = '''
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\\n...\\n-----END PRIVATE KEY-----\\n",
  "client_email": "...",
  "client_id": "...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "..."
}
'''
```

**Önemli:**
- JSON içindeki `\n` karakterlerini `\\n` olarak değiştirin
- Tüm JSON içeriğini tek bir string olarak ekleyin
- Google Sheets setup için `GOOGLE_SHEETS_SETUP.md` dosyasına bakın

### 4. Google Sheets Hazırlama

Google Sheets entegrasyonu için:

1. `GOOGLE_SHEETS_SETUP.md` dosyasındaki adımları takip edin
2. Gerekli sheet'leri oluşturun:
   - `Vehicles`
   - `FuelLevels`
   - `ExteriorChecks`
   - `EngineChecks`
   - `SafetyEquipment`
   - `InteriorChecks`
   - `Items`
   - `Users`
   - `Submissions`

### 5. Uygulamayı Test Etme

1. Deploy işlemi tamamlandıktan sonra uygulamanızı açın
2. Login sayfasında test kullanıcıları ile giriş yapın
3. Form gönderimi yapın ve Google Sheets'te kontrol edin

## Diğer Bulut Platformları

### Heroku

1. `Procfile` oluşturun:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

2. Environment variables olarak secrets ekleyin:
```bash
heroku config:set USE_GOOGLE_SHEETS=true
heroku config:set GOOGLE_SHEET_ID=your_sheet_id
heroku config:set GOOGLE_CREDENTIALS_JSON='{...}'
```

### Docker

1. `Dockerfile` oluşturun:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

2. Environment variables ile çalıştırın:
```bash
docker run -p 8501:8501 \
  -e USE_GOOGLE_SHEETS=true \
  -e GOOGLE_SHEET_ID=your_sheet_id \
  -e GOOGLE_CREDENTIALS_JSON='{...}' \
  your-image-name
```

## Sorun Giderme

### Google Sheets Bağlantı Hatası

- Service account email'ine Google Sheets'te erişim verdiğinizden emin olun
- `GOOGLE_SHEET_ID`'nin doğru olduğundan emin olun
- `GOOGLE_CREDENTIALS_JSON` formatının doğru olduğundan emin olun

### Veri Kaybolması

- Google Sheets kullanıyorsanız veriler kalıcıdır
- Excel fallback kullanıyorsanız, bulut ortamında dosyalar geçicidir
- Her zaman Google Sheets kullanmanız önerilir

### Login Sorunları

- `Users` sheet'inin Google Sheets'te mevcut olduğundan emin olun
- Kullanıcı bilgilerinin doğru formatta olduğundan emin olun

## Yerel Geliştirme

Yerel geliştirme için:

1. `.streamlit/secrets.toml` dosyası oluşturun (`.streamlit/secrets.toml.example` dosyasını kopyalayın)
2. Secrets'ları doldurun
3. `streamlit run app.py` komutu ile çalıştırın

**Not:** Yerel geliştirmede Excel dosyaları kullanılabilir, ancak bulut ortamında Google Sheets kullanmanız önerilir.

