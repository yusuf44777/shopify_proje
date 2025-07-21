import json
import os
import subprocess
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Model configuration
def get_available_models():
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

AVAILABLE_MODELS = get_available_models()
DEFAULT_MODEL = "shopify-gpt" if "shopify-gpt" in AVAILABLE_MODELS else (AVAILABLE_MODELS[0] if AVAILABLE_MODELS else "llama2")

def generate_with_ollama(prompt, model_name, language="English"):
    """Ollama ile içerik oluştur"""
    try:
        # Dil spesifik prompt hazırla
        if language.lower() in ['turkish', 'türkçe']:
            system_prompt = """Sen ShopifyGPT'sin, Shopify ürün açıklamaları konusunda uzman bir AI asistanısın. 
            Etkileyici, SEO optimize edilmiş, dönüşüm odaklı Türkçe ürün açıklamaları oluşturursun."""
            full_prompt = f"Türkçe olarak şu ürün için kapsamlı Shopify ürün açıklaması oluştur: {prompt}"
        else:
            system_prompt = """You are ShopifyGPT, an expert AI assistant specialized in creating compelling Shopify product descriptions. 
            You create engaging, SEO-optimized, conversion-focused product descriptions in English."""
            full_prompt = f"Create a comprehensive Shopify product description for: {prompt}"
        
        # Tam prompt
        complete_prompt = f"{system_prompt}\n\n{full_prompt}"
        
        # Ollama ile yanıt oluştur
        cmd = ['ollama', 'run', model_name, complete_prompt]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
        else:
            return f"Error: {result.stderr}"
        
    except subprocess.TimeoutExpired:
        return "Error: Timeout - işlem çok uzun sürdü"
    except Exception as e:
        return f"Error: {str(e)}"

# HTML Template for web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ShopifyGPT API</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { 
            max-width: 1200px; 
            margin: 0 auto; 
            background: white; 
            border-radius: 20px; 
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; 
            padding: 40px; 
            text-align: center; 
        }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .header p { font-size: 1.2em; opacity: 0.9; }
        .content { padding: 40px; }
        .form-group { margin-bottom: 25px; }
        label { 
            display: block; 
            margin-bottom: 8px; 
            font-weight: 600; 
            color: #333;
        }
        input, textarea, select { 
            width: 100%; 
            padding: 15px; 
            border: 2px solid #e1e5e9; 
            border-radius: 10px; 
            font-size: 16px;
            transition: all 0.3s ease;
        }
        input:focus, textarea:focus, select:focus { 
            outline: none; 
            border-color: #667eea; 
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        textarea { height: 120px; resize: vertical; }
        .btn { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; 
            padding: 15px 30px; 
            border: none; 
            border-radius: 10px; 
            font-size: 16px; 
            font-weight: 600;
            cursor: pointer; 
            transition: all 0.3s ease;
            width: 100%;
        }
        .btn:hover { 
            transform: translateY(-2px); 
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }
        .result { 
            margin-top: 30px; 
            padding: 25px; 
            background: #f8f9fa; 
            border-radius: 10px; 
            display: none;
            border-left: 5px solid #667eea;
        }
        .result h3 { 
            color: #333; 
            margin-bottom: 15px; 
            font-size: 1.3em;
        }
        .result-content { 
            background: white; 
            padding: 20px; 
            border-radius: 8px; 
            border: 1px solid #e1e5e9;
            white-space: pre-wrap;
            line-height: 1.6;
        }
        .loading { 
            display: none; 
            text-align: center; 
            padding: 20px;
            color: #667eea;
        }
        .spinner { 
            border: 3px solid #f3f3f3; 
            border-top: 3px solid #667eea; 
            border-radius: 50%; 
            width: 30px; 
            height: 30px; 
            animation: spin 1s linear infinite; 
            margin: 0 auto 10px;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        @media (max-width: 768px) { .grid { grid-template-columns: 1fr; } }
        .api-info {
            background: #e8f4fd;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            border-left: 5px solid #3498db;
        }
        .api-info h3 { color: #2c3e50; margin-bottom: 10px; }
        .api-info code { 
            background: #34495e; 
            color: #ecf0f1; 
            padding: 2px 6px; 
            border-radius: 4px; 
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 ShopifyGPT API</h1>
            <p>Ollama ile eğitilmiş özel Shopify ürün açıklama AI'ınız</p>
        </div>
        
        <div class="content">
            <div class="api-info">
                <h3>📡 API Bilgileri</h3>
                <p><strong>Endpoint:</strong> <code>POST /generate</code></p>
                <p><strong>Model:</strong> <code>{{ model_name }}</code></p>
                <p><strong>Durum:</strong> <span id="model-status">Kontrol ediliyor...</span></p>
            </div>

            <div class="grid">
                <div>
                    <h2>🛍️ Ürün Açıklaması Oluştur</h2>
                    <form id="generateForm">
                        <div class="form-group">
                            <label for="prompt">Ürün Bilgisi:</label>
                            <textarea id="prompt" name="prompt" placeholder="Örn: wireless bluetooth headphones with noise cancellation" required></textarea>
                        </div>
                        
                        <div class="form-group">
                            <label for="language">Dil:</label>
                            <select id="language" name="language">
                                <option value="English">English</option>
                                <option value="Turkish">Türkçe</option>
                            </select>
                        </div>
                        
                        <button type="submit" class="btn">🚀 Açıklama Oluştur</button>
                    </form>
                </div>
                
                <div>
                    <h2>📊 Sonuç</h2>
                    <div class="loading" id="loading">
                        <div class="spinner"></div>
                        <p>ShopifyGPT ile açıklama oluşturuluyor...</p>
                    </div>
                    
                    <div class="result" id="result">
                        <h3>✅ Oluşturulan Açıklama</h3>
                        <div class="result-content" id="resultContent"></div>
                        <button onclick="copyToClipboard()" class="btn" style="margin-top: 15px; width: auto;">📋 Kopyala</button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Model durumunu kontrol et
        fetch('/health')
            .then(response => response.json())
            .then(data => {
                const statusElement = document.getElementById('model-status');
                if (data.status === 'healthy') {
                    statusElement.innerHTML = '<span style="color: #27ae60;">✅ Aktif</span>';
                } else {
                    statusElement.innerHTML = '<span style="color: #e74c3c;">❌ Erişilemez</span>';
                }
            })
            .catch(() => {
                document.getElementById('model-status').innerHTML = '<span style="color: #e74c3c;">❌ Hata</span>';
            });

        // Form submit işlemi
        document.getElementById('generateForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const prompt = document.getElementById('prompt').value;
            const language = document.getElementById('language').value;
            
            // Loading göster
            document.getElementById('loading').style.display = 'block';
            document.getElementById('result').style.display = 'none';
            
            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        prompt: prompt,
                        language: language
                    })
                });
                
                const data = await response.json();
                
                // Loading gizle
                document.getElementById('loading').style.display = 'none';
                
                if (data.success) {
                    document.getElementById('resultContent').textContent = data.description;
                    document.getElementById('result').style.display = 'block';
                } else {
                    alert('Hata: ' + data.error);
                }
                
            } catch (error) {
                document.getElementById('loading').style.display = 'none';
                alert('Bağlantı hatası: ' + error.message);
            }
        });
        
        // Panoya kopyala
        function copyToClipboard() {
            const content = document.getElementById('resultContent').textContent;
            navigator.clipboard.writeText(content).then(() => {
                alert('📋 İçerik panoya kopyalandı!');
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Ana sayfa - Web arayüzü"""
    return render_template_string(HTML_TEMPLATE, model_name=DEFAULT_MODEL, available_models=AVAILABLE_MODELS)

@app.route('/generate', methods=['POST'])
def generate_description():
    """Ürün açıklaması oluştur"""
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        language = data.get('language', 'English')
        model_name = data.get('model', DEFAULT_MODEL)
        
        if not prompt:
            return jsonify({'success': False, 'error': 'Prompt gerekli'}), 400
        
        # Model kontrolü
        if model_name not in AVAILABLE_MODELS:
            model_name = DEFAULT_MODEL
        
        # Ollama ile yanıt oluştur
        result = generate_with_ollama(prompt, model_name, language)
        
        if result and not result.startswith("Error"):
            return jsonify({
                'success': True,
                'description': result,
                'model': model_name,
                'language': language,
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({'success': False, 'error': result}), 500
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Model sağlık kontrolü"""
    try:
        # Varsayılan model ile test
        test_result = generate_with_ollama("Test", DEFAULT_MODEL)
        if test_result and not test_result.startswith("Error"):
            return jsonify({
                'status': 'healthy', 
                'model': DEFAULT_MODEL,
                'available_models': AVAILABLE_MODELS,
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'status': 'unhealthy',
                'error': 'Model test failed',
                'timestamp': datetime.now().isoformat()
            }), 500
    except Exception as e:
        return jsonify({
            'status': 'unhealthy', 
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/info', methods=['GET'])
def api_info():
    """API bilgileri"""
    return jsonify({
        'name': 'ShopifyGPT API',
        'version': '1.0.0',
        'model': DEFAULT_MODEL,
        'available_models': AVAILABLE_MODELS,
        'endpoints': {
            '/': 'GET - Web arayüzü',
            '/generate': 'POST - Ürün açıklaması oluştur',
            '/health': 'GET - Sağlık kontrolü',
            '/info': 'GET - API bilgileri',
            '/models': 'GET - Mevcut modeller'
        },
        'example_request': {
            'url': '/generate',
            'method': 'POST',
            'body': {
                'prompt': 'wireless bluetooth headphones',
                'language': 'English',
                'model': DEFAULT_MODEL
            }
        },
        'timestamp': datetime.now().isoformat()
    })

@app.route('/models', methods=['GET'])
def list_models():
    """Mevcut Ollama modellerini listele"""
    try:
        fresh_models = get_available_models()
        return jsonify({
            'models': fresh_models,
            'current_model': DEFAULT_MODEL,
            'count': len(fresh_models),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# CORS desteği için
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

if __name__ == '__main__':
    print("🚀 ShopifyGPT API sunucusu başlatılıyor...")
    print(f"📋 Varsayılan Model: {DEFAULT_MODEL}")
    print(f"🤖 Mevcut Modeller: {', '.join(AVAILABLE_MODELS) if AVAILABLE_MODELS else 'Hiçbiri'}")
    print(f"🌐 Web Arayüzü: http://localhost:5000")
    print(f"📡 API Endpoint: http://localhost:5000/generate")
    print(f"❤️ Sağlık Kontrolü: http://localhost:5000/health")
    print("=" * 50)
    
    if not AVAILABLE_MODELS:
        print("⚠️ Hiçbir Ollama modeli bulunamadı!")
        print("💡 Model indirmek için: ollama pull llama2")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
