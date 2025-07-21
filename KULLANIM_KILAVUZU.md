# 🛍️ Shopify-GPT Sistemi - Kullanım Kılavuzu

## 🎯 Sistem Özeti

Shopify-GPT sisteminiz artık tamamen operasyonel! Bu sistem size özel olarak eğitilmiş AI modelleri ile Shopify ürün açıklamaları oluşturmanıza olanak sağlar.

## 🤖 Mevcut AI Modelleri

### 1. **Shopify-GPT (Önerilen)**
- **Model Adı**: `shopify-gpt:latest`
- **Boyut**: 4.9 GB
- **Özellik**: Shopify e-ticaret içeriklerine özel olarak eğitilmiş
- **Dil Desteği**: Türkçe ve İngilizce
- **Optimizasyon**: SEO odaklı, dönüşüm artırıcı içerik

### 2. **Llama 3.2 (Genel Amaçlı)**
- **Model Adı**: `llama3.2:latest`
- **Boyut**: 2.0 GB
- **Özellik**: Hızlı ve verimli genel AI modeli

### 3. **Llama 3.1 8B (Güçlü)**
- **Model Adı**: `llama3.1:8b`
- **Boyut**: 4.9 GB
- **Özellik**: Yüksek kaliteli metin üretimi

## 🚀 Sistem Kullanımı

### Web Arayüzü (Streamlit)
1. Tarayıcınızda `http://localhost:8501` adresine gidin
2. Sol panelde "Ollama" seçeneğini seçin
3. "Shopify-GPT" modelini seçin
4. Ürün anahtar kelimesini girin
5. Dili seçin (Türkçe/İngilizce)
6. "🚀 Açıklama Oluştur" butonuna tıklayın

### Terminal Kullanımı
```bash
# Direkt model kullanımı
ollama run shopify-gpt "kablosuz kulaklık için ürün açıklaması oluştur"

# Pipeline ile kullanım
echo "fitness tracker için açıklama" | ollama run shopify-gpt
```

### Python API Kullanımı
```python
import subprocess

def generate_with_shopify_gpt(prompt, language="Türkçe"):
    if language == "Türkçe":
        full_prompt = f"Türkçe olarak {prompt} için Shopify ürün açıklaması oluştur."
    else:
        full_prompt = f"Create a Shopify product description for {prompt}."
    
    cmd = ['ollama', 'run', 'shopify-gpt', full_prompt]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        return f"Error: {result.stderr}"

# Kullanım örneği
description = generate_with_shopify_gpt("kablosuz mouse")
print(description)
```

## 📊 Özellikler

### ✅ Desteklenen Özellikler
- **Çoklu AI Sağlayıcı**: OpenAI, Google Gemini, Ollama
- **Offline Çalışma**: Ollama modelleri internet gerektirmez
- **SEO Optimizasyon**: Anahtar kelime entegrasyonu
- **HTML Çıktı**: Shopify'a hazır format
- **Çok Dilli**: Türkçe ve İngilizce destek
- **İçerik Analizi**: Kelime sayısı, karakter sayısı
- **Kopyalama/İndirme**: Sonuçları kolayca paylaşın

### 🎨 Çıktı Formatı
- Başlık hiyerarşisi (H1, H2, H3)
- Emoji kullanımı
- Bullet pointler
- Call-to-action bölümleri
- SEO dostu yapı

## 🔧 Gelişmiş Kullanım

### Yeni Model Eğitimi
```bash
# Model trainer çalıştırma
python model_trainer.py

# Kendi verilerinizle eğitim
# model_training_data/ klasörüne JSON dosyalarınızı ekleyin
```

### API Server Başlatma
```bash
# Flask API sunucusu
python shopify_api.py

# API endpoint'leri:
# POST /generate - Açıklama oluştur
# GET /health - Sistem durumu
# GET / - API bilgileri
```

## 🛠️ Troubleshooting

### Model Bulunamadı Hatası
```bash
# Modelleri kontrol et
ollama list

# Eksik model indir
ollama pull shopify-gpt
```

### Streamlit Çalışmıyor
```bash
# Eski prosesleri kapat
pkill -f streamlit

# Yeniden başlat
streamlit run shopify.py
```

### Model Yanıt Vermiyor
```bash
# Ollama servisini yeniden başlat
ollama serve

# Model durumunu kontrol et
ollama ps
```

## 📈 Performans Optimizasyonu

### Hız İyileştirme
- Daha küçük modeller kullanın (llama3.2)
- Prompt uzunluğunu optimize edin
- Sistem kaynaklarını kontrol edin

### Kalite İyileştirme
- Shopify-GPT modelini tercih edin
- Spesifik anahtar kelimeler kullanın
- Uzun promptlar verin

## 🎯 En İyi Uygulamalar

### Prompt Yazma İpuçları
```
❌ Kötü: "ürün açıklaması yaz"
✅ İyi: "kablosuz bluetooth kulaklık için SEO optimize edilmiş Türkçe ürün açıklaması oluştur"

❌ Kötü: "mouse"
✅ İyi: "gaming mouse RGB aydınlatmalı ergonomik tasarım"
```

### Çıktı Kullanımı
- HTML formatını direkt Shopify'a kopyalayın
- SEO anahtar kelimeleri kontrol edin
- Call-to-action bölümlerini özelleştirin

## 🎉 Başarı! Sistem Hazır

Shopify-GPT sisteminiz tamamen operasyonel. Artık:
- ✅ Offline AI model çalışıyor
- ✅ Web arayüzü aktif
- ✅ Terminal komutları hazır
- ✅ API entegrasyonu mevcut
- ✅ Eğitim sistemi kurulu

**Web Arayüzü**: http://localhost:8501
**Model Adı**: shopify-gpt:latest
**Durum**: 🟢 Aktif

Artık profesyonel Shopify ürün açıklamaları oluşturabilirsiniz! 🚀
