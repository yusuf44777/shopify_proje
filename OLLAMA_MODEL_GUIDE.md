# 🤖 ShopifyGPT - Ollama Model Seçimi Rehberi

## 🆕 Yeni Özellikler

Artık ShopifyGPT sisteminizde herhangi bir Ollama modelini kullanabilirsiniz! Sistem otomatik olarak mevcut modellerinizi algılar ve seçim yapmanıza olanak tanır.

## 🚀 Hızlı Başlangıç

### 1. Popüler Modelleri İndirin

```bash
# Temel modeller
ollama pull llama2        # Facebook'un temel modeli
ollama pull llama3        # Güncel ve güçlü
ollama pull llama3.1      # En son sürüm
ollama pull llama3.2      # En yeni versiyon

# Özelleşmiş modeller  
ollama pull mistral       # Hızlı ve etkili
ollama pull mixtral       # Çoklu uzman model
ollama pull gemma         # Google'ın modeli
ollama pull gemma2        # Güncellenmiş versiyon

# Kod odaklı modeller
ollama pull codellama     # Kod yazmak için
ollama pull deepseek-coder # Gelişmiş kod modeli

# Hafif modeller
ollama pull phi3          # Microsoft'un küçük modeli
ollama pull qwen2         # Çin kaynaklı etkili model
```

### 2. Sistemin Yeni Özellikleri

#### A) Veri Toplama - AI Zenginleştirme
```bash
python data_collector.py
```
- Sistem mevcut Ollama modellerinizi listeler
- Hangi model ile veriyi zenginleştirmek istediğinizi seçebilirsiniz
- AI model ürün açıklamalarını otomatik olarak iyileştirir

#### B) Model Eğitimi - Temel Model Seçimi  
```bash
python model_trainer.py
```
- Farklı temel modeller arasından seçim yapabilirsiniz
- llama2, llama3, mistral, qwen2 gibi seçenekler
- Sistem otomatik olarak eksik modelleri indirir

#### C) Arayüz - Dinamik Model Seçimi
```bash
streamlit run shopify_gpt_interface.py
```
- Sol panelde mevcut tüm modellerinizi görebilirsiniz
- İstediğiniz modeli anında değiştirebilirsiniz
- Model performansını karşılaştırabilirsiniz

#### D) API - Çoklu Model Desteği
```bash
python shopify_api.py
```
- API isteklerinde model parametresi ile istediğiniz modeli belirtebilirsiniz
- Dinamik model listesi
- Model durumu kontrolü

## 📊 Model Karşılaştırması

### Hız vs Kalite Matrisi

| Model | Hız | Kalite | RAM | Özellik |
|-------|-----|--------|-----|---------|
| **llama3.2** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 8GB | En güncel |
| **llama3.1** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 8GB | Stabil |
| **llama3** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 4GB | Dengeli |
| **mistral** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 4GB | Hızlı |
| **gemma2** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 6GB | Google |
| **qwen2.5** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 4GB | Çok dilli |
| **phi3** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 2GB | Hafif |

### Önerilen Kullanım Senaryoları

#### 🏆 En İyi Kalite: llama3.2 veya llama3.1
```bash
ollama pull llama3.2
# Kullanım: Yüksek kaliteli, detaylı açıklamalar
```

#### ⚡ En Hızlı: mistral veya phi3  
```bash
ollama pull mistral
# Kullanım: Hızlı toplu üretim
```

#### 🌍 Çok Dilli: qwen2.5
```bash
ollama pull qwen2.5
# Kullanım: Türkçe ve diğer diller
```

#### 💻 Düşük RAM: phi3
```bash
ollama pull phi3
# Kullanım: Sınırlı donanım
```

## 🔧 Yeni API Kullanımı

### Model Seçerek İstek

```bash
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "wireless headphones",
    "language": "Turkish", 
    "model": "llama3.2"
  }'
```

### Mevcut Modelleri Listele

```bash
curl http://localhost:5000/models
```

### Model Durumu Kontrol

```bash
curl http://localhost:5000/health
```

## 📱 Yeni Arayüz Özellikleri

### Streamlit Arayüzü

1. **Model Seçici**: Sol panelde dropdown menu
2. **Model Durumu**: Anlık model bilgisi  
3. **Karşılaştırma**: Farklı modelleri yan yana test
4. **Performans**: Model hızı ve kalite metrikleri

### Web API Arayüzü

1. **Model Dropdown**: Web sayfasında model seçimi
2. **Dinamik Liste**: Otomatik model keşfi
3. **Responsive**: Mobil uyumlu tasarım

## 🎯 Pratik Örnekler

### Senaryo 1: Hızlı Toplu Üretim

```bash
# Hızlı model indirme
ollama pull mistral

# Veri toplama (mistral ile zenginleştirme)
python data_collector.py
# → Model seçimi: mistral

# Üretim (mistral ile)
python shopify_gpt_interface.py
# → Model seçimi: mistral
```

### Senaryo 2: En İyi Kalite

```bash
# En iyi model indirme  
ollama pull llama3.2

# Model eğitimi (llama3.2 temel)
python model_trainer.py
# → Temel model: llama3.2

# Kendi ShopifyGPT modelinizi kullanın
python shopify_gpt_interface.py
# → Model seçimi: shopify-gpt
```

### Senaryo 3: Çoklu Model Test

```bash
# Birden fazla model indirin
ollama pull llama3
ollama pull mistral  
ollama pull gemma2

# Karşılaştırma yapın
python shopify_gpt_interface.py
# → "Model Karşılaştırması" sekmesi
```

## 🚨 Sorun Giderme

### Model Bulunamadı Hatası

```bash
# Mevcut modelleri kontrol edin
ollama list

# Model indirin
ollama pull llama2

# Servisi yeniden başlatın
ollama serve
```

### Bellek Hatası

```bash
# Daha hafif model kullanın
ollama pull phi3

# Veya model parametrelerini düşürün
# (model_trainer.py içinde temperature, context vb.)
```

### API Bağlantı Hatası

```bash
# Ollama servisini başlatın
ollama serve

# Port kontrolü
lsof -i :11434
```

## 🔄 Güncellemeler

### Son Değişiklikler

- ✅ Dinamik model keşfi
- ✅ Model seçimi UI'ları
- ✅ API model parametresi
- ✅ Karşılaştırma özelliği  
- ✅ Performans metrikleri
- ✅ AI veri zenginleştirme

### Gelecek Özellikler

- 🔮 Model konfigürasyon editörü
- 🔮 Otomatik model önerisi
- 🔮 A/B test desteği
- 🔮 Model performans analizi

## 📞 Destek

Herhangi bir sorunuz varsa:
- 📧 Email: mahiryusufacan@gmail.com  
- 🐙 GitHub: [@yusuf44777](https://github.com/yusuf44777)
- 📋 Issues: Proje repository'sinde

---

🎉 Artık istediğiniz Ollama modeli ile ShopifyGPT'yi kullanabilirsiniz!
