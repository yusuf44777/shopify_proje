# 🤖 ShopifyGPT - Kendi AI Modeliniz

Ollama ile eğitilmiş özel Shopify ürün açıklama AI'ınız. Bu proje ile kendi verilerinizi toplayarak, özelleştirilmiş bir AI model eğitebilir ve Shopify mağazanız için benzersiz ürün açıklamaları oluşturabilirsiniz.

## 🌟 Özellikler

- **🔍 Otomatik Veri Toplama**: Shopify sitelerinden ürün verilerini otomatik toplama
- **🤖 Özel Model Eğitimi**: Ollama ile kendi AI modelinizi eğitme
- **🌐 Çoklu Dil Desteği**: Türkçe ve İngilizce ürün açıklamaları
- **📊 Model Karşılaştırması**: Farklı AI modelleri arasında performans karşılaştırması
- **🎨 Modern Arayüz**: Streamlit ile kullanıcı dostu web arayüzü
- **⚡ Hızlı API**: Flask tabanlı RESTful API

## 🚀 Hızlı Başlangıç

### 1. Kurulum

```bash
# Projeyi klonlayın
git clone https://github.com/yusuf44777/shopify_proje.git
cd shopify_proje

# Otomatik kurulum scriptini çalıştırın
chmod +x setup_shopify_gpt.sh
./setup_shopify_gpt.sh
```

### 2. Manuel Kurulum (İsteğe Bağlı)

```bash
# Virtual environment oluşturun
python3 -m venv shopify_gpt_env
source shopify_gpt_env/bin/activate

# Gereksinimleri yükleyin
pip install -r requirements_ollama.txt

# Ollama'yı kurun (macOS)
curl -fsSL https://ollama.ai/install.sh | sh

# Temel modeli indirin
ollama pull llama2
```

## 📋 Kullanım Adımları

### 1. Veri Toplama

```bash
python data_collector.py
```

Bu script:
- Shopify sitelerini otomatik bulur
- Ürün bilgilerini toplar
- Verileri JSON/CSV formatında kaydeder

### 2. Veri İşleme

```bash
python data_preprocessor.py
```

Bu script:
- Ham verileri temizler
- Eğitim formatına dönüştürür
- Eğitim/doğrulama setlerini ayırır

### 3. Model Eğitimi

```bash
python model_trainer.py
```

Bu script:
- Ollama ile özel model oluşturur
- ShopifyGPT modelini eğitir
- Model performansını test eder

### 4. Arayüz Kullanımı

```bash
# Streamlit arayüzü
streamlit run shopify_gpt_interface.py

# API sunucusu
python shopify_api.py
```

## 🔧 Proje Yapısı

```
shopify_proje/
├── 📄 shopify.py                    # Orijinal Streamlit uygulaması
├── 🔍 data_collector.py             # Veri toplama scripti
├── 🔄 data_preprocessor.py          # Veri işleme scripti
├── 🤖 model_trainer.py              # Model eğitim scripti
├── 🖥️ shopify_gpt_interface.py      # ShopifyGPT arayüzü
├── 🌐 shopify_api.py                # Flask API (oluşturulacak)
├── 📦 requirements.txt              # Orijinal gereksinimler
├── 📦 requirements_ollama.txt       # Ollama gereksinimleri
├── 🚀 setup_shopify_gpt.sh          # Kurulum scripti
├── 📁 shopify_training_data/        # Ham veri dizini
├── 📁 model_training_data/          # İşlenmiş veri dizini
└── 📁 logs/                         # Log dosyaları
```

## 🎯 Model Eğitim Süreci

### 1. Veri Toplama Stratejisi

- **Kaynak Çeşitliliği**: Farklı kategorilerden Shopify siteleri
- **Veri Kalitesi**: HTML temizleme ve normalizasyon
- **Ölçeklenebilirlik**: Rate limiting ve error handling

### 2. Model Mimarisi

```python
# Modelfile örneği
FROM llama2

SYSTEM "ShopifyGPT system prompt..."

PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER top_k 40
```

### 3. Eğitim Formatı

```json
{
  "instruction": "Create a Shopify product description for:",
  "input": "wireless bluetooth headphones",
  "output": "Comprehensive product description...",
  "task_type": "description_generation"
}
```

## 📊 Model Performansı

- **Veri Seti Boyutu**: 1000+ ürün açıklaması
- **Eğitim Süresi**: ~30-60 dakika (donanıma bağlı)
- **Dil Desteği**: Türkçe ve İngilizce
- **Çıktı Kalitesi**: SEO optimize, HTML formatında

## 🔌 API Kullanımı

### REST API Endpoints

```bash
# Ürün açıklaması oluştur
POST /generate
{
  "prompt": "wireless earbuds",
  "language": "Turkish"
}

# Sağlık kontrolü
GET /health

# Model bilgisi
GET /
```

### Python API Kullanımı

```python
import ollama

response = ollama.chat(
    model='shopify-gpt',
    messages=[{
        'role': 'user', 
        'content': 'Create a product description for smart watch'
    }]
)

print(response['message']['content'])
```

## 🛠️ Geliştirme

### Ortam Değişkenleri

```bash
# .env dosyası
OPENAI_API_KEY=your_openai_key
GEMINI_API_KEY=your_gemini_key
```

### Veri Toplama Özelleştirmesi

```python
# data_collector.py içinde
keywords = [
    "fashion+clothing",
    "electronics+gadgets", 
    "home+decor"
    # Kendi kategorilerinizi ekleyin
]
```

### Model Hiperparametreleri

```python
# model_trainer.py içinde
PARAMETER temperature 0.7      # Yaratıcılık
PARAMETER top_p 0.9           # Çeşitlilik  
PARAMETER top_k 40            # Kelime seçimi
PARAMETER num_predict 2048    # Maksimum token
```

## 🎨 Arayüz Özellikleri

- **Modern Design**: Gradyent renkler ve responsive tasarım
- **Gerçek Zamanlı Üretim**: Canlı içerik oluşturma
- **Model Karşılaştırması**: Farklı AI modelleri yan yana
- **Düzenleme**: Oluşturulan içeriği düzenleme
- **Export**: HTML/Text formatında indirme

## 📈 Performans Optimizasyonu

### Veri Toplama
- Paralel scraping
- Rate limiting
- User agent rotation
- Error handling

### Model Eğitimi
- Batch processing
- Memory management
- Checkpoint saving
- Validation monitoring

### Arayüz
- Caching
- Lazy loading
- Error boundaries
- Progress indicators

## 🔒 Güvenlik

- API rate limiting
- Input validation
- XSS protection
- Environment variables

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Commit edin (`git commit -m 'Add some AmazingFeature'`)
4. Push edin (`git push origin feature/AmazingFeature`)
5. Pull Request açın

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakın.

## 👨‍💻 Geliştirici

**Mahir Yusuf Acan**
- GitHub: [@yusuf44777](https://github.com/yusuf44777)
- Email: mahiryusufacan@gmail.com

## 🙏 Teşekkürler

- [Ollama](https://ollama.ai/) - Local AI model runtime
- [Streamlit](https://streamlit.io/) - Web app framework
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - Web scraping
- [Selenium](https://selenium.dev/) - Browser automation

## 📚 Ek Kaynaklar

- [Ollama Dokümantasyonu](https://ollama.ai/docs)
- [Shopify API Kılavuzu](https://shopify.dev/api)
- [AI Model Fine-tuning](https://huggingface.co/docs/transformers/training)

---

⭐ Bu projeyi beğendiyseniz star vermeyi unutmayın!
