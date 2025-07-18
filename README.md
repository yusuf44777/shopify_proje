# Shopify Product Description Generator

Bu uygulama, Shopify mağazaları için AI destekli ürün açıklamaları oluşturmanıza yardımcı olur. OpenAI ve Google Gemini API'lerini kullanarak SEO optimizasyonlu, dönüşüm odaklı HTML açıklamaları üretir.

## Özellikler

- 🤖 **Dual AI Support**: OpenAI (GPT-4, GPT-3.5) ve Google Gemini desteği
- 🛍️ **Shopify Optimized**: Shopify kurallarına uygun HTML çıktısı
- 📱 **Responsive Interface**: Kullanıcı dostu Streamlit arayüzü
- ✂️ **Edit & Copy**: Sonuçları düzenleyebilme ve kopyalayabilme
- 📥 **Download**: HTML dosyası olarak indirme
- 🎯 **SEO Optimized**: Arama motoru optimizasyonu için tasarlanmış

## Kurulum

1. **Gerekli paketleri yükleyin:**
```bash
pip install streamlit openai google-generativeai python-dotenv
```

2. **API anahtarlarınızı yapılandırın:**
   - `.env.example` dosyasını `.env` olarak kopyalayın
   - API anahtarlarınızı ekleyin (isteğe bağlı - uygulama içinde de girebilirsiniz)

## Kullanım

1. **Uygulamayı başlatın:**
```bash
streamlit run shopify.py
```

2. **API Yapılandırması:**
   - Sol menüden OpenAI veya Gemini'yi seçin
   - API anahtarınızı girin

3. **Açıklama Oluşturma:**
   - Ürün keyword'ünü girin (örn: "wireless bluetooth headphones")
   - "Generate Description" butonuna tıklayın

4. **Sonucu Kullanma:**
   - **Edit Tab**: Açıklamayı düzenleyin
   - **Preview Tab**: HTML önizlemesini görün
   - **Copy Tab**: HTML kodunu kopyalayın veya indirin

## API Anahtarları Nasıl Alınır?

### OpenAI API Key:
1. [OpenAI Platform](https://platform.openai.com/) hesabınıza giriş yapın
2. API Keys bölümüne gidin
3. "Create new secret key" butonuna tıklayın

### Google Gemini API Key:
1. [Google AI Studio](https://makersuite.google.com/app/apikey) sayfasına gidin
2. "Create API Key" butonuna tıklayın
3. Projenizi seçin veya yeni bir proje oluşturun

## Çıktı Formatı

Oluşturulan açıklamalar şunları içerir:
- **H1**: Ürün başlığı
- **H2**: Ana özellikler ve faydalar
- **H3**: Ürün detayları
- **H4**: Teknik özellikler (gerekirse)
- **HTML**: Shopify'a uygun temiz HTML kodu

## Kullanım İpuçları

- Spesifik keyword'ler kullanın ("ayakkabı" yerine "su geçirmez hiking botu")
- Marka adlarını dahil edin
- Hedef kitlenizi düşünün
- Sonucu kendi markanıza göre düzenleyin

## Teknik Detaylar

- **Frontend**: Streamlit
- **AI Providers**: OpenAI GPT, Google Gemini
- **Output Format**: Shopify-optimized HTML
- **Features**: Real-time editing, HTML preview, file download

## Güvenlik

- API anahtarları güvenli bir şekilde saklanır
- `.env` dosyası git'e dahil edilmez
- Anahtarlar sadece geçerli oturum için bellekte tutulur

## Destek

Herhangi bir sorun yaşarsanız:
1. API anahtarlarınızın doğru olduğundan emin olun
2. İnternet bağlantınızı kontrol edin
3. Konsol hatalarını kontrol edin

## Lisans

Bu proje MIT lisansı altında dağıtılmaktadır.
