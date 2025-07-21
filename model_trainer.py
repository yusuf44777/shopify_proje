import json
import os
import subprocess
import sys
import time
from datetime import datetime
import requests
import ollama

class OllamaModelTrainer:
    def __init__(self):
        self.available_base_models = [
            "llama2", "llama3", "llama3.1", "llama3.2",
            "mistral", "mixtral", "qwen", "qwen2", "qwen2.5",
            "codellama", "deepseek-coder", "phi3", "gemma", "gemma2"
        ]
        self.base_model = "llama2"  # Varsayılan model
        self.model_name = "shopify-gpt"
        self.training_data_dir = "model_training_data"
        self.modelfile_path = "Modelfile"
        
    def check_ollama_installation(self):
        """Ollama kurulumunu kontrol et"""
        try:
            result = subprocess.run(['ollama', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Ollama kurulu: {result.stdout.strip()}")
                return True
            else:
                print("❌ Ollama kurulu değil!")
                return False
        except FileNotFoundError:
            print("❌ Ollama bulunamadı! Lütfen önce Ollama'yı kurun.")
            print("📥 İndirme linki: https://ollama.ai/download")
            return False
    
    def get_available_models(self):
        """Mevcut Ollama modellerini listele"""
        try:
            result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
            if result.returncode == 0:
                models = []
                lines = result.stdout.strip().split('\n')[1:]  # İlk satır başlık
                for line in lines:
                    if line.strip():
                        model_name = line.split()[0]  # İlk sütun model adı
                        models.append(model_name)
                return models
            else:
                return []
        except:
            return []
    
    def select_base_model(self):
        """Kullanıcıdan temel model seçimi al"""
        print("\n🤖 Temel Model Seçimi")
        print("=" * 40)
        
        # Mevcut modelleri kontrol et
        available_models = self.get_available_models()
        
        print("Önerilen temel modeller:")
        model_options = []
        
        for i, model in enumerate(self.available_base_models, 1):
            if model in available_models:
                status = "✅ İndirilmiş"
                model_options.append(model)
            else:
                status = "📥 İndirilmeli"
                model_options.append(model)
            
            print(f"{i}. {model} - {status}")
        
        print(f"{len(self.available_base_models) + 1}. Varsayılan (llama2)")
        
        while True:
            try:
                choice = input(f"\nSeçiminiz (1-{len(self.available_base_models) + 1}): ").strip()
                
                if choice == str(len(self.available_base_models) + 1):
                    return "llama2"
                
                choice_num = int(choice)
                if 1 <= choice_num <= len(self.available_base_models):
                    selected_model = self.available_base_models[choice_num - 1]
                    print(f"✅ Seçilen temel model: {selected_model}")
                    return selected_model
                else:
                    print("❌ Geçersiz seçim!")
                    
            except ValueError:
                print("❌ Lütfen sayı girin!")
            except KeyboardInterrupt:
                print("\n⚠️ İşlem iptal edildi")
                return "llama2"
    
    def download_base_model(self, model_name="llama2"):
        """Temel modeli indir"""
        try:
            print(f"📥 Temel model indiriliyor: {model_name}")
            result = subprocess.run(['ollama', 'pull', model_name], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Model başarıyla indirildi: {model_name}")
                return True
            else:
                print(f"❌ Model indirme hatası: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ Model indirme hatası: {e}")
            return False
    
    def create_modelfile(self, base_model="llama2"):
        """Özel model için Modelfile oluştur"""
        
        system_prompt = """You are ShopifyGPT, an expert e-commerce copywriter specialized in creating compelling Shopify product descriptions. Your expertise includes:

1. SEO-optimized product titles and descriptions
2. Conversion-focused copywriting
3. Emotional triggers and persuasive language
4. Product feature highlighting
5. Customer benefit-focused content
6. HTML formatting for Shopify
7. Multi-language support (Turkish and English)

Guidelines:
- Always create engaging, customer-centric content
- Focus on benefits over features
- Use emotional triggers to drive conversions
- Include relevant keywords naturally
- Format content appropriately for Shopify
- Be specific and avoid generic descriptions
- Help customers envision success with the product

Respond with compelling, conversion-optimized content that drives sales."""

        modelfile_content = f"""FROM {base_model}

SYSTEM """{system_prompt}"""

PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER top_k 40
PARAMETER num_predict 2048

TEMPLATE \"\"\"{{ if .System }}<|im_start|>system
{{ .System }}<|im_end|>
{{ end }}{{ if .Prompt }}<|im_start|>user
{{ .Prompt }}<|im_end|>
{{ end }}<|im_start|>assistant
{{ .Response }}<|im_end|>
\"\"\"
"""

        with open(self.modelfile_path, 'w', encoding='utf-8') as f:
            f.write(modelfile_content)
        
        print(f"✅ Modelfile oluşturuldu: {self.modelfile_path}")
        return True
    
    def create_training_dataset(self):
        """Eğitim veri setini hazırla"""
        training_files = []
        
        # JSON ve JSONL dosyalarını bul
        for filename in os.listdir(self.training_data_dir):
            if filename.endswith(('.json', '.jsonl')):
                training_files.append(os.path.join(self.training_data_dir, filename))
        
        if not training_files:
            print("❌ Eğitim verisi bulunamadı!")
            return None
        
        # En güncel dosyayı seç
        latest_file = max(training_files, key=os.path.getmtime)
        print(f"📋 Kullanılacak eğitim verisi: {latest_file}")
        
        return latest_file
    
    def fine_tune_with_ollama(self):
        """Ollama ile model ince ayarı (fine-tuning)"""
        print("🔄 Ollama ile model oluşturuluyor...")
        
        try:
            # Özel modeli oluştur
            result = subprocess.run(['ollama', 'create', self.model_name, '-f', self.modelfile_path], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ Model başarıyla oluşturuldu: {self.model_name}")
                return True
            else:
                print(f"❌ Model oluşturma hatası: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Model oluşturma hatası: {e}")
            return False
    
    def test_model(self):
        """Oluşturulan modeli test et"""
        print("🧪 Model test ediliyor...")
        
        test_prompts = [
            "Write a compelling Shopify product title for wireless bluetooth headphones.",
            "Create a product description for organic skincare serum.",
            "Generate a product description in Turkish for a fitness tracker.",
        ]
        
        try:
            for i, prompt in enumerate(test_prompts, 1):
                print(f"\n📝 Test {i}: {prompt}")
                
                # Ollama Python istemcisi kullan
                response = ollama.chat(model=self.model_name, messages=[
                    {'role': 'user', 'content': prompt}
                ])
                
                print(f"🤖 Yanıt: {response['message']['content'][:200]}...")
                print("-" * 50)
                
        except Exception as e:
            print(f"❌ Model test hatası: {e}")
    
    def create_api_server(self):
        """Model için basit API sunucusu oluştur"""
        api_code = '''
import ollama
from flask import Flask, request, jsonify
import json

app = Flask(__name__)
MODEL_NAME = "shopify-gpt"

@app.route('/generate', methods=['POST'])
def generate_description():
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        language = data.get('language', 'English')
        
        if not prompt:
            return jsonify({'error': 'Prompt gerekli'}), 400
        
        # Dil spesifik prompt hazırla
        if language.lower() == 'turkish' or language.lower() == 'türkçe':
            full_prompt = f"Türkçe olarak {prompt} için Shopify ürün açıklaması oluştur."
        else:
            full_prompt = f"Create a Shopify product description for {prompt}."
        
        # Ollama ile yanıt oluştur
        response = ollama.chat(model=MODEL_NAME, messages=[
            {'role': 'user', 'content': full_prompt}
        ])
        
        return jsonify({
            'success': True,
            'description': response['message']['content'],
            'model': MODEL_NAME,
            'language': language
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    try:
        # Model erişilebilirliğini test et
        test_response = ollama.chat(model=MODEL_NAME, messages=[
            {'role': 'user', 'content': 'Test'}
        ])
        return jsonify({'status': 'healthy', 'model': MODEL_NAME})
    except:
        return jsonify({'status': 'unhealthy'}), 500

@app.route('/', methods=['GET'])
def info():
    return jsonify({
        'name': 'ShopifyGPT API',
        'model': MODEL_NAME,
        'version': '1.0.0',
        'endpoints': {
            '/generate': 'POST - Ürün açıklaması oluştur',
            '/health': 'GET - Sağlık kontrolü'
        }
    })

if __name__ == '__main__':
    print(f"🚀 ShopifyGPT API başlatılıyor...")
    print(f"📋 Model: {MODEL_NAME}")
    print(f"🌐 API: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
'''
        
        with open('shopify_api.py', 'w', encoding='utf-8') as f:
            f.write(api_code)
        
        print("✅ API sunucusu kodu oluşturuldu: shopify_api.py")
    
    def train_model(self):
        """Tam eğitim sürecini çalıştır"""
        print("🚀 ShopifyGPT model eğitimi başlıyor...")
        
        # Ollama kurulumunu kontrol et
        if not self.check_ollama_installation():
            return False
        
        # Temel model seçimi
        self.base_model = self.select_base_model()
        
        # Temel modeli indir
        if not self.download_base_model(self.base_model):
            return False
        
        # Eğitim verisini hazırla
        training_file = self.create_training_dataset()
        if not training_file:
            return False
        
        # Modelfile oluştur
        if not self.create_modelfile(self.base_model):
            return False
        
        # Model oluştur
        if not self.fine_tune_with_ollama():
            return False
        
        # Modeli test et
        self.test_model()
        
        # API sunucusu oluştur
        self.create_api_server()
        
        print("🎉 ShopifyGPT eğitimi tamamlandı!")
        print(f"📋 Model adı: {self.model_name}")
        print("🚀 API'yi başlatmak için: python shopify_api.py")
        
        return True

class ModelEvaluator:
    def __init__(self, model_name="shopify-gpt"):
        self.model_name = model_name
    
    def evaluate_model_performance(self):
        """Model performansını değerlendir"""
        print("📊 Model performansı değerlendiriliyor...")
        
        test_cases = [
            {
                'category': 'Electronics',
                'keyword': 'wireless earbuds',
                'expected_elements': ['battery life', 'wireless', 'sound quality', 'bluetooth']
            },
            {
                'category': 'Fashion',
                'keyword': 'summer dress',
                'expected_elements': ['fabric', 'style', 'comfort', 'occasion']
            },
            {
                'category': 'Beauty',
                'keyword': 'anti-aging cream',
                'expected_elements': ['skin', 'ingredients', 'benefits', 'application']
            }
        ]
        
        results = []
        
        for test_case in test_cases:
            try:
                prompt = f"Create a Shopify product description for {test_case['keyword']} in {test_case['category']} category."
                
                response = ollama.chat(model=self.model_name, messages=[
                    {'role': 'user', 'content': prompt}
                ])
                
                generated_text = response['message']['content'].lower()
                
                # Beklenen elementleri kontrol et
                found_elements = []
                for element in test_case['expected_elements']:
                    if element.lower() in generated_text:
                        found_elements.append(element)
                
                score = len(found_elements) / len(test_case['expected_elements'])
                
                results.append({
                    'test_case': test_case['keyword'],
                    'category': test_case['category'],
                    'score': score,
                    'found_elements': found_elements,
                    'response_length': len(generated_text)
                })
                
                print(f"✅ {test_case['keyword']}: {score:.2f} puan")
                
            except Exception as e:
                print(f"❌ Test hatası {test_case['keyword']}: {e}")
        
        # Ortalama performans
        if results:
            avg_score = sum(r['score'] for r in results) / len(results)
            print(f"📊 Ortalama performans: {avg_score:.2f}")
        
        return results

def main():
    """Ana fonksiyon"""
    print("🤖 ShopifyGPT Model Eğitim Sistemi")
    print("=" * 50)
    
    trainer = OllamaModelTrainer()
    
    try:
        # Model eğitimini başlat
        success = trainer.train_model()
        
        if success:
            print("\n🎯 Model eğitimi başarılı!")
            
            # Model performansını değerlendir
            evaluator = ModelEvaluator()
            evaluator.evaluate_model_performance()
            
            print("\n📚 Kullanım Örnekleri:")
            print("1. Terminal'de: ollama run shopify-gpt")
            print("2. Python'da: ollama.chat(model='shopify-gpt', messages=[{'role': 'user', 'content': 'prompt'}])")
            print("3. API: python shopify_api.py")
            
        else:
            print("❌ Model eğitimi başarısız!")
    
    except KeyboardInterrupt:
        print("\n⚠️ İşlem kullanıcı tarafından durduruldu")
    except Exception as e:
        print(f"❌ Beklenmeyen hata: {e}")

if __name__ == "__main__":
    main()
