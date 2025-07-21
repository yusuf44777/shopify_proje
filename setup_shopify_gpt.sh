#!/bin/bash

# ShopifyGPT Kurulum ve Çalıştırma Scripti
# Mahir Yusuf Acan tarafından hazırlanmıştır

echo "🚀 ShopifyGPT Kurulum ve Eğitim Sistemi"
echo "======================================="

# Renk kodları
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Hata kontrolü fonksiyonu
check_command() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ $1 başarılı${NC}"
    else
        echo -e "${RED}❌ $1 başarısız${NC}"
        exit 1
    fi
}

# Python versiyonu kontrolü
echo -e "${BLUE}🐍 Python versiyonu kontrol ediliyor...${NC}"
python3 --version
check_command "Python kontrolü"

# Ollama kurulum kontrolü
echo -e "${BLUE}🤖 Ollama kurulumu kontrol ediliyor...${NC}"
if ! command -v ollama &> /dev/null; then
    echo -e "${YELLOW}⚠️ Ollama bulunamadı. Kuruluyor...${NC}"
    
    # macOS için Ollama kurulumu
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo -e "${BLUE}🍎 macOS için Ollama kuruluyor...${NC}"
        curl -fsSL https://ollama.ai/install.sh | sh
        check_command "Ollama kurulumu"
    else
        echo -e "${RED}❌ Manuel Ollama kurulumu gerekli: https://ollama.ai/download${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✅ Ollama zaten kurulu${NC}"
    ollama --version
fi

# Virtual environment oluşturma
echo -e "${BLUE}📦 Virtual environment oluşturuluyor...${NC}"
python3 -m venv shopify_gpt_env
check_command "Virtual environment oluşturma"

# Virtual environment aktifleştirme
echo -e "${BLUE}🔄 Virtual environment aktifleştiriliyor...${NC}"
source shopify_gpt_env/bin/activate
check_command "Virtual environment aktifleştirme"

# Gereksinimleri yükleme
echo -e "${BLUE}📚 Python kütüphaneleri yükleniyor...${NC}"
pip install --upgrade pip
pip install -r requirements_ollama.txt
check_command "Kütüphane yüklemesi"

# ChromeDriver kurulumu (macOS için)
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo -e "${BLUE}🌐 ChromeDriver kontrol ediliyor...${NC}"
    if ! command -v chromedriver &> /dev/null; then
        echo -e "${YELLOW}⚠️ ChromeDriver bulunamadı. Homebrew ile kuruluyor...${NC}"
        if command -v brew &> /dev/null; then
            brew install --cask chromedriver
            check_command "ChromeDriver kurulumu"
        else
            echo -e "${YELLOW}⚠️ Homebrew bulunamadı. ChromeDriver'ı manuel kurmanız gerekebilir${NC}"
        fi
    else
        echo -e "${GREEN}✅ ChromeDriver zaten kurulu${NC}"
    fi
fi

# Temel model indirme
echo -e "${BLUE}🤖 Temel Ollama modeli indiriliyor...${NC}"
ollama pull llama2
check_command "Temel model indirme"

# Dizin yapısını oluşturma
echo -e "${BLUE}📁 Proje dizinleri oluşturuluyor...${NC}"
mkdir -p shopify_training_data
mkdir -p model_training_data
mkdir -p logs
check_command "Dizin oluşturma"

echo -e "${GREEN}🎉 Kurulum tamamlandı!${NC}"
echo ""
echo -e "${BLUE}📋 Kullanım Adımları:${NC}"
echo "1. ${YELLOW}Veri Toplama:${NC} python data_collector.py"
echo "2. ${YELLOW}Veri İşleme:${NC} python data_preprocessor.py"
echo "3. ${YELLOW}Model Eğitimi:${NC} python model_trainer.py"
echo "4. ${YELLOW}ShopifyGPT Arayüzü:${NC} streamlit run shopify_gpt_interface.py"
echo ""
echo -e "${BLUE}🔧 Manuel Komutlar:${NC}"
echo "• Virtual env aktifleştir: ${YELLOW}source shopify_gpt_env/bin/activate${NC}"
echo "• Ollama başlat: ${YELLOW}ollama serve${NC}"
echo "• Model listele: ${YELLOW}ollama list${NC}"
echo "• Model test et: ${YELLOW}ollama run shopify-gpt${NC}"
echo ""
echo -e "${GREEN}✨ ShopifyGPT kullanıma hazır!${NC}"
