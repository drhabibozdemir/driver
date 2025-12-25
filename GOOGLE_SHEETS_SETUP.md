# Google Sheets Entegrasyonu Kurulum Rehberi

Streamlit Cloud'da form gönderimlerini kalıcı olarak saklamak için Google Sheets kullanabilirsiniz.

## Adım 1: Google Cloud Console'da Proje Oluşturma

1. [Google Cloud Console](https://console.cloud.google.com/)'a gidin
2. Yeni bir proje oluşturun veya mevcut bir projeyi seçin
3. **APIs & Services** > **Library**'ye gidin
4. Şu API'leri etkinleştirin:
   - **Google Sheets API**
   - **Google Drive API**

## Adım 2: Service Account Oluşturma

1. **APIs & Services** > **Credentials**'a gidin
2. **Create Credentials** > **Service Account**'u seçin
3. Service account adı verin (örn: "streamlit-driver-app")
4. **Create and Continue**'a tıklayın
5. Role olarak **Editor** seçin (veya gerekli izinleri verin)
6. **Done**'a tıklayın

## Adım 3: Service Account Key İndirme

1. Oluşturduğunuz service account'a tıklayın
2. **Keys** sekmesine gidin
3. **Add Key** > **Create new key**'i seçin
4. Format olarak **JSON** seçin
5. **Create**'e tıklayın - JSON dosyası indirilecek

## Adım 4: Google Sheets Oluşturma

1. [Google Sheets](https://sheets.google.com/)'e gidin
2. Yeni bir spreadsheet oluşturun
3. İlk sheet'i "Submissions" olarak yeniden adlandırın
4. Spreadsheet'in URL'sinden Sheet ID'yi kopyalayın:
   - URL formatı: `https://docs.google.com/spreadsheets/d/SHEET_ID_HERE/edit`
   - `SHEET_ID_HERE` kısmını kopyalayın

## Adım 5: Service Account'a Erişim Verme

1. Google Sheets'te **Share** butonuna tıklayın
2. İndirdiğiniz JSON dosyasındaki `client_email` değerini kopyalayın
3. Bu email adresini Google Sheets'e **Editor** yetkisiyle ekleyin
4. **Send**'e tıklayın

## Adım 6: Streamlit Cloud Secrets Ayarlama

1. Streamlit Cloud'da uygulamanızın sayfasına gidin
2. **Settings** > **Secrets**'e tıklayın
3. Aşağıdaki formatı kullanarak secrets ekleyin:

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
- İndirdiğiniz JSON dosyasının tüm içeriğini `GOOGLE_CREDENTIALS_JSON` içine yapıştırın
- JSON içindeki tüm `\n` karakterlerini `\\n` olarak değiştirin
- `GOOGLE_SHEET_ID`'yi Adım 4'te kopyaladığınız ID ile değiştirin

## Adım 7: Uygulamayı Yeniden Deploy Etme

1. Secrets'ı kaydettikten sonra uygulama otomatik olarak yeniden deploy edilir
2. Veya manuel olarak **Reboot app** butonuna tıklayın

## Test Etme

1. Uygulamada bir form gönderin
2. Google Sheets'te "Submissions" sheet'ine gidin
3. Verilerin eklendiğini kontrol edin

## Sorun Giderme

- **"Permission denied" hatası:** Service account email'ine Google Sheets'te erişim verdiğinizden emin olun
- **"Sheet not found" hatası:** GOOGLE_SHEET_ID'nin doğru olduğundan emin olun
- **"Invalid credentials" hatası:** GOOGLE_CREDENTIALS_JSON'un doğru formatta olduğundan emin olun (\\n karakterleri önemli)

## Alternatif: Excel Dosyası Kullanımı (Geliştirme)

Google Sheets kullanmak istemiyorsanız, `USE_GOOGLE_SHEETS = "false"` olarak ayarlayın. 
Ancak Streamlit Cloud'da dosya sistemi geçici olduğu için veriler deploy'lar arasında kaybolabilir.

