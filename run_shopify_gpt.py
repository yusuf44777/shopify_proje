#!/usr/bin/env python3
"""
ShopifyGPT Çalıştırıcı Script
Tüm bileşenleri sıralı olarak çalıştırır
"""

import subprocess
import sys
import os
import time
from pathlib import Path

def run_command(command, description):
    """Komutu çalıştır ve sonucu göster"""
    print(f"\n🔄 {description}")
    print(f"Komut: {command}")
    print("-" * 50)
    
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=False, text=True)
        print(f"✅ {description} başarılı!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} başarısız!")
        print(f"Hata: {e}")
        return False
    except KeyboardInterrupt:
        print(f"\n⚠️ {description} kullanıcı tarafından durduruldu")
        return False

def check_requirements():
    """Gereksinimleri kontrol et"""
    print("📋 Gereksinimler kontrol ediliyor...")
    
    required_files = [
        "data_collector.py",
        "data_preprocessor.py", 
        "model_trainer.py",
        "shopify_gpt_interface.py",
        "requirements_ollama.txt"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Eksik dosyalar: {missing_files}")
        return False
    
    print("✅ Tüm dosyalar mevcut")
    return True

def setup_environment():
    """Çevre ortamını ayarla"""
    print("🔧 Çevre ortamı ayarlanıyor...")
    
    # Dizinleri oluştur
    dirs = ["shopify_training_data", "model_training_data", "logs"]
    for dir_name in dirs:
        os.makedirs(dir_name, exist_ok=True)
        print(f"📁 Dizin oluşturuldu: {dir_name}")
    
    return True

def main():
    """Ana fonksiyon"""
    print("🤖 ShopifyGPT Otomatik Çalıştırıcı")
    print("=" * 50)
    
    # Gereksinimleri kontrol et
    if not check_requirements():
        sys.exit(1)
    
    # Çevre ortamını ayarla
    if not setup_environment():
        sys.exit(1)
    
    # Kullanıcıdan seçim al
    print("\n📋 Ne yapmak istiyorsunuz?")
    print("1. Tam süreç (veri toplama → işleme → eğitim)")
    print("2. Sadece veri toplama")
    print("3. Sadece veri işleme")
    print("4. Sadece model eğitimi")
    print("5. ShopifyGPT arayüzü başlat")
    print("6. API sunucusu başlat")
    print("0. Çıkış")
    
    choice = input("\nSeçiminiz (1-6): ").strip()
    
    if choice == "0":
        print("👋 Çıkılıyor...")
        sys.exit(0)
    
    elif choice == "1":
        print("🚀 Tam süreç başlatılıyor...")
        
        # 1. Veri toplama
        print("\n" + "="*50)
        print("📊 1. AŞAMA: Veri Toplama")
        if not run_command("python3 data_collector.py", "Veri toplama"):
            print("❌ Veri toplama başarısız, devam edilemiyor")
            sys.exit(1)
        
        # 2. Veri işleme
        print("\n" + "="*50)
        print("🔄 2. AŞAMA: Veri İşleme")
        if not run_command("python3 data_preprocessor.py", "Veri işleme"):
            print("❌ Veri işleme başarısız, devam edilemiyor")
            sys.exit(1)
        
        # 3. Model eğitimi
        print("\n" + "="*50)
        print("🤖 3. AŞAMA: Model Eğitimi")
        if not run_command("python3 model_trainer.py", "Model eğitimi"):
            print("❌ Model eğitimi başarısız")
            sys.exit(1)
        
        print("\n🎉 Tam süreç başarıyla tamamlandı!")
        
        # Arayüz başlatma önerisi
        start_interface = input("\nShopifyGPT arayüzünü başlatmak ister misiniz? (y/n): ").lower()
        if start_interface == 'y':
            run_command("streamlit run shopify_gpt_interface.py", "ShopifyGPT arayüzü")
    
    elif choice == "2":
        run_command("python3 data_collector.py", "Veri toplama")
    
    elif choice == "3":
        run_command("python3 data_preprocessor.py", "Veri işleme")
    
    elif choice == "4":
        run_command("python3 model_trainer.py", "Model eğitimi")
    
    elif choice == "5":
        print("🖥️ ShopifyGPT arayüzü başlatılıyor...")
        print("🌐 Tarayıcınızda http://localhost:8501 adresini açın")
        run_command("streamlit run shopify_gpt_interface.py", "ShopifyGPT arayüzü")
    
    elif choice == "6":
        print("🌐 API sunucusu başlatılıyor...")
        print("🔗 API: http://localhost:5000")
        run_command("python3 shopify_api.py", "API sunucusu")
    
    else:
        print("❌ Geçersiz seçim!")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️ İşlem kullanıcı tarafından durduruldu")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Beklenmeyen hata: {e}")
        sys.exit(1)
