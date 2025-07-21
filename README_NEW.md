# 🛍️ Shopify-GPT Sistemi

> **Offline çalışabilen, Shopify'a özel eğitilmiş AI sistemi ile profesyonel ürün açıklamaları oluşturun!**

## 🎯 Sistem Özellikleri

- **🤖 Özel AI Modeli**: Shopify e-ticaret içeriklerine özel eğitilmiş
- **🌐 Web Arayüzü**: Kullanıcı dostu Streamlit uygulaması
- **📱 Offline Çalışma**: İnternet bağlantısı gerektirmez
- **🌍 Çok Dilli**: Türkçe ve İngilizce destek
- **⚡ Hızlı Üretim**: 15-30 saniyede profesyonel açıklama
- **📊 İçerik Analizi**: SEO metrikleri ve istatistikler

## 🚀 Hızlı Başlangıç

### 1. Sistem Durumu Kontrolü
```bash
python system_status.py
```

### 2. Web Arayüzü
```bash
# Tarayıcıda açın: http://localhost:8501
streamlit run shopify.py
```

### 3. Terminal Kullanımı
```bash
ollama run shopify-gpt "kablosuz kulaklık için ürün açıklaması"
```

## 🏗️ Kurulum (Tamamlandı)

✅ **Ollama AI Platform**: Kurulu ve çalışır  
✅ **Shopify-GPT Modeli**: Eğitildi ve aktif  
✅ **Python Bağımlılıkları**: Yüklü  
✅ **Web Arayüzü**: Çalışır durumda  
✅ **Eğitim Verisi**: Hazırlandı  

## 🎨 Özellikler

### AI Modelleri
- **Shopify-GPT**: E-ticaret içeriklerine özel (4.9 GB)
- **Llama 3.2**: Hızlı genel model (2.0 GB)  
- **Llama 3.1 8B**: Yüksek kalite (4.9 GB)

### Web Arayüzü
- Çoklu AI sağlayıcı (OpenAI, Gemini, Ollama)
- Model seçim menüsü
- Dil seçimi (TR/EN)
- İçerik analizi
- HTML export

### API & CLI
- REST API endpoints
- Terminal komutları
- Python entegrasyonu
- Batch processing

## 📊 Sistem Durumu

```bash
🛍️ Shopify-GPT Sistem Durumu
✅ Ollama Servisi: Aktif
✅ Streamlit Uygulaması: Çalışıyor  
✅ Shopify-GPT Modeli: Hazır
✅ Eğitim Verisi: Mevcut
```

## 🔧 Kullanım Örnekleri

### Web Arayüzü
1. http://localhost:8501 adresine gidin
2. "Ollama" > "shopify-gpt" seçin
3. "kablosuz mouse" yazın
4. "Açıklama Oluştur" tıklayın

### Python Kodu
```python
import subprocess

def generate_description(product):
    cmd = ['ollama', 'run', 'shopify-gpt', f'{product} için ürün açıklaması']
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()

# Kullanım
desc = generate_description("fitness tracker")
print(desc)
```

## 📁 Proje Dosyaları

| Dosya | Açıklama |
|-------|----------|
| `shopify.py` | Ana Streamlit uygulaması |
| `shopify-gpt` | Özel eğitilmiş AI modeli |
| `model_trainer.py` | Model eğitim sistemi |
| `system_status.py` | Durum kontrol dashboard |
| `KULLANIM_KILAVUZU.md` | Detaylı kullanım kılavuzu |

## 🎯 Çıktı Örnekleri

### Türkçe Çıktı
```html
<h1>🎧 Premium Kablosuz Bluetooth Kulaklık</h1>
<p>Müziğinizi hiç olmadığı kadar kaliteli dinleyin...</p>
<h2>🎯 Neden Bu Ürünü Tercih Etmelisiniz?</h2>
<ul>
  <li>30 saatlik batarya ömrü</li>
  <li>Aktif gürültü engelleme</li>
  <li>Hi-Fi ses kalitesi</li>
</ul>
```

### English Output  
```html
<h1>🎧 Premium Wireless Bluetooth Headphones</h1>
<p>Experience music like never before with our cutting-edge...</p>
<h2>🎯 Why Choose This Product?</h2>
<ul>
  <li>30-hour battery life</li>
  <li>Active noise cancellation</li>
  <li>Hi-Fi sound quality</li>
</ul>
```

## 📈 Performans

- **Model Boyutu**: 4.9 GB
- **Yanıt Süresi**: 15-30 saniye
- **Dil Desteği**: TR + EN
- **Platform**: macOS (M1/M2 optimize)
- **Offline**: ✅ Tam destek

## 🛠️ Troubleshooting

### Model Bulunamadı
```bash
ollama list | grep shopify
# Eğer boşsa:
ollama pull shopify-gpt
```

### Streamlit Çalışmıyor
```bash
pkill -f streamlit
streamlit run shopify.py
```

### Sistem Kontrolü
```bash
python system_status.py
```

## 🎊 Sonuç

**🎉 Shopify-GPT sisteminiz tamamen çalışır durumda!**

- **Web**: http://localhost:8501
- **Model**: shopify-gpt:latest  
- **Durum**: 🟢 Aktif ve Hazır

Artık profesyonel Shopify ürün açıklamaları oluşturabilirsiniz! 🚀
