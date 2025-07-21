#!/usr/bin/env python3
"""
Shopify-GPT Sistem Durumu Dashboard
Bu script sistemin mevcut durumunu kontrol eder ve rapor verir.
"""

import subprocess
import requests
import json
import os
from datetime import datetime

def check_ollama_status():
    """Ollama servis durumunu kontrol et"""
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, "Ollama çalışmıyor"
    except FileNotFoundError:
        return False, "Ollama kurulu değil"

def check_streamlit_status():
    """Streamlit uygulaması durumunu kontrol et"""
    try:
        response = requests.get('http://localhost:8501', timeout=5)
        if response.status_code == 200:
            return True, "Streamlit aktif"
        else:
            return False, f"HTTP {response.status_code}"
    except requests.exceptions.RequestException:
        return False, "Streamlit erişilemiyor"

def check_shopify_gpt_model():
    """Shopify-GPT modelinin varlığını kontrol et"""
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if 'shopify-gpt' in result.stdout:
            return True, "Shopify-GPT modeli mevcut"
        else:
            return False, "Shopify-GPT modeli bulunamadı"
    except:
        return False, "Model kontrolü başarısız"

def test_model_response():
    """Model yanıt verme kabiliyetini test et"""
    try:
        test_prompt = "test için kısa açıklama"
        cmd = ['ollama', 'run', 'shopify-gpt', test_prompt]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        
        if result.returncode == 0 and len(result.stdout.strip()) > 10:
            return True, "Model başarıyla yanıt veriyor"
        else:
            return False, "Model yanıt vermiyor"
    except subprocess.TimeoutExpired:
        return False, "Model timeout"
    except:
        return False, "Test başarısız"

def check_training_data():
    """Eğitim verisi varlığını kontrol et"""
    data_dir = "model_training_data"
    if os.path.exists(data_dir):
        files = [f for f in os.listdir(data_dir) if f.endswith(('.json', '.jsonl'))]
        if files:
            return True, f"{len(files)} eğitim dosyası mevcut"
        else:
            return False, "Eğitim dosyası bulunamadı"
    else:
        return False, "Eğitim klasörü yok"

def main():
    """Ana dashboard fonksiyonu"""
    print("🛍️ Shopify-GPT Sistem Durumu Dashboard")
    print("=" * 50)
    print(f"📅 Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Sistem kontrolleri
    checks = [
        ("🤖 Ollama Servisi", check_ollama_status),
        ("🌐 Streamlit Uygulaması", check_streamlit_status),
        ("🏷️ Shopify-GPT Modeli", check_shopify_gpt_model),
        ("⚡ Model Test", test_model_response),
        ("📊 Eğitim Verisi", check_training_data),
    ]
    
    all_good = True
    
    for check_name, check_func in checks:
        try:
            status, message = check_func()
            if status:
                print(f"✅ {check_name}: {message}")
            else:
                print(f"❌ {check_name}: {message}")
                all_good = False
        except Exception as e:
            print(f"❌ {check_name}: Hata - {e}")
            all_good = False
    
    print("\n" + "=" * 50)
    
    if all_good:
        print("🎉 Tüm sistemler çalışıyor! Shopify-GPT kullanıma hazır.")
        print("\n📋 Hızlı Başlangıç:")
        print("• Web Arayüzü: http://localhost:8501")
        print("• Terminal: ollama run shopify-gpt")
        print("• Model: shopify-gpt:latest")
    else:
        print("⚠️ Bazı sistemlerde sorunlar var. Lütfen hataları kontrol edin.")
        print("\n🔧 Sorun Giderme:")
        print("• Ollama: ollama serve")
        print("• Streamlit: streamlit run shopify.py")
        print("• Model: ollama pull shopify-gpt")
    
    # Detaylı model bilgileri
    print("\n📋 Mevcut Modeller:")
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if 'shopify-gpt' in line.lower():
                    print(f"🎯 {line}")
                elif any(model in line.lower() for model in ['llama', 'mistral', 'gemma']):
                    print(f"📦 {line}")
        else:
            print("❌ Model listesi alınamadı")
    except:
        print("❌ Model kontrolü başarısız")

if __name__ == "__main__":
    main()
