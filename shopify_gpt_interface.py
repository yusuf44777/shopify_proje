import streamlit as st
import json
import os
import subprocess
from datetime import datetime

class ShopifyGPTInterface:
    def __init__(self):
        self.model_name = "shopify-gpt"
        self.available_models = self.get_available_models()
        self.selected_model = self.model_name if self.model_name in self.available_models else None
    
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
    
    def check_model_availability(self):
        """ShopifyGPT modelinin mevcut olup olmadığını kontrol et"""
        return self.model_name in self.available_models
    
    def generate_with_ollama(self, prompt, model_name, language="English", temperature=0.7):
        """Ollama ile içerik oluştur"""
        try:
            # Dil spesifik prompt hazırla
            if language.lower() in ['türkçe', 'turkish']:
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
    
    def compare_models(self, prompt, language="English"):
        """Farklı modelleri karşılaştır"""
        results = {}
        
        # Mevcut modellerin tümünü test et
        comparison_models = self.available_models[:5]  # İlk 5 model
        
        for model in comparison_models:
            try:
                results[model] = self.generate_with_ollama(prompt, model, language)
            except:
                results[model] = "Model erişilemedi"
        
        return results

def main():
    st.set_page_config(
        page_title="ShopifyGPT - Kendi AI Modeliniz",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .model-status {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .model-available {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    .model-unavailable {
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
    .comparison-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #007bff;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🤖 ShopifyGPT - Kendi AI Modeliniz</h1>
        <p>Ollama ile eğitilmiş özel Shopify ürün açıklama AI'ınız</p>
    </div>
    """, unsafe_allow_html=True)
    
    # ShopifyGPT interface'ini başlat
    shopify_gpt = ShopifyGPTInterface()
    
    # Sidebar - Model bilgileri
    with st.sidebar:
        st.header("🔧 Model Bilgileri")
        
        # Model seçimi
        if shopify_gpt.available_models:
            selected_model = st.selectbox(
                "🤖 Kullanılacak Model:",
                options=shopify_gpt.available_models,
                index=0 if shopify_gpt.available_models else None,
                help="Kullanmak istediğiniz Ollama modelini seçin"
            )
            shopify_gpt.selected_model = selected_model
            
            st.success(f"✅ Seçili Model: {selected_model}")
        else:
            st.error("❌ Hiçbir Ollama modeli bulunamadı")
            st.markdown("""
            **Model indirmek için:**
            ```bash
            ollama pull llama2
            ollama pull mistral
            ollama pull llama3
            ```
            """)
        
        st.markdown("---")
        
        # Mevcut modeller
        st.subheader("📋 Mevcut Ollama Modelleri")
        if shopify_gpt.available_models:
            for model in shopify_gpt.available_models:
                if model == "shopify-gpt":
                    st.success(f"🤖 {model} (Özel Model)")
                else:
                    st.info(f"📦 {model}")
        else:
            st.warning("Hiçbir Ollama modeli bulunamadı")
        
        st.markdown("---")
        
        # Model ayarları
        st.subheader("⚙️ Model Ayarları")
        temperature = st.slider(
            "Yaratıcılık (Temperature)",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Yüksek değerler daha yaratıcı, düşük değerler daha tutarlı sonuçlar verir"
        )
    
    # Ana içerik
    if not shopify_gpt.available_models:
        st.error("🚨 Hiçbir Ollama modeli bulunamadı!")
        st.markdown("### 📚 Model İndirme Adımları:")
        st.code("""
# Popüler modelleri indirin
ollama pull llama2
ollama pull llama3
ollama pull mistral
ollama pull gemma

# Kendi ShopifyGPT modelinizi eğitin
python model_trainer.py
        """, language="bash")
        return
    
    # Ana uygulama
    tab1, tab2, tab3 = st.tabs(["🚀 Üretim", "⚖️ Model Karşılaştırma", "📊 Performans"])
    
    with tab1:
        st.header("🛍️ Ürün Açıklaması Üretimi")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Dil seçimi
            language = st.selectbox(
                "📢 Çıktı Dili:",
                ["English", "Türkçe"],
                index=0
            )
            
            # Ürün bilgileri
            product_input = st.text_area(
                "🏷️ Ürün Bilgisi:",
                placeholder="Örn: wireless bluetooth headphones with noise cancellation",
                height=100,
                help="Ürün adı, kategori veya anahtar kelimeler girin"
            )
            
            # Üretim butonu
            if st.button("🚀 Açıklama Üret", type="primary", disabled=not product_input.strip() or not shopify_gpt.selected_model):
                with st.spinner(f"{shopify_gpt.selected_model} ile açıklama oluşturuluyor..."):
                    result = shopify_gpt.generate_with_ollama(
                        product_input, 
                        shopify_gpt.selected_model,
                        language, 
                        temperature
                    )
                    
                    if result and not result.startswith("Error"):
                        st.session_state['shopify_gpt_result'] = result
                        st.session_state['product_input'] = product_input
                        st.session_state['used_model'] = shopify_gpt.selected_model
                        st.success("✅ Açıklama başarıyla oluşturuldu!")
                    else:
                        st.error(f"❌ Hata: {result}")
        
        with col2:
            # Sonuçları göster
            if 'shopify_gpt_result' in st.session_state:
                st.subheader("📝 Oluşturulan Açıklama")
                
                # Kullanılan model bilgisi
                used_model = st.session_state.get('used_model', 'Bilinmiyor')
                st.info(f"🤖 Kullanılan Model: **{used_model}**")
                
                result_tabs = st.tabs(["📖 Metin", "🔧 Düzenle", "📋 Kopyala"])
                
                with result_tabs[0]:
                    st.markdown(st.session_state['shopify_gpt_result'])
                
                with result_tabs[1]:
                    edited_result = st.text_area(
                        "Açıklamayı düzenleyin:",
                        value=st.session_state['shopify_gpt_result'],
                        height=300
                    )
                    if st.button("💾 Güncelle"):
                        st.session_state['shopify_gpt_result'] = edited_result
                        st.success("Güncellendi!")
                
                with result_tabs[2]:
                    st.code(st.session_state['shopify_gpt_result'], language='html')
                    
                    # İndirme
                    filename = f"shopify_description_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
                    st.download_button(
                        label="📥 HTML İndir",
                        data=st.session_state['shopify_gpt_result'],
                        file_name=filename,
                        mime="text/html"
                    )
    
    with tab2:
        st.header("⚖️ Model Karşılaştırması")
        st.write("ShopifyGPT'yi diğer modellerle karşılaştırın")
        
        comparison_input = st.text_input(
            "🔍 Karşılaştırma için ürün:",
            placeholder="wireless earbuds"
        )
        
        comparison_language = st.selectbox(
            "Karşılaştırma dili:",
            ["English", "Türkçe"],
            key="comparison_lang"
        )
        
        if st.button("🔄 Modelleri Karşılaştır", disabled=not comparison_input.strip()):
            with st.spinner("Modeller karşılaştırılıyor..."):
                results = shopify_gpt.compare_models(comparison_input, comparison_language)
                
                for model_name, result in results.items():
                    st.markdown(f"""
                    <div class="comparison-box">
                        <h4>🤖 {model_name}</h4>
                        <p>{result[:300]}{"..." if len(result) > 300 else ""}</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    with tab3:
        st.header("📊 Model Performansı")
        
        if st.button("🧪 Performans Testi Çalıştır"):
            with st.spinner("Model performansı test ediliyor..."):
                # Basit performans testi
                test_prompts = [
                    "wireless bluetooth headphones",
                    "organic face cream", 
                    "fitness tracker watch"
                ]
                
                if shopify_gpt.selected_model:
                    results = []
                    for prompt in test_prompts:
                        result = shopify_gpt.generate_with_ollama(prompt, shopify_gpt.selected_model)
                        results.append({
                            'prompt': prompt,
                            'length': len(result),
                            'words': len(result.split()),
                            'has_html': '<' in result and '>' in result
                        })
                    
                    # Sonuçları göster
                    st.subheader("📈 Test Sonuçları")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        avg_length = sum(r['length'] for r in results) / len(results)
                        st.metric("Ortalama Karakter", f"{avg_length:.0f}")
                    
                    with col2:
                        avg_words = sum(r['words'] for r in results) / len(results)
                        st.metric("Ortalama Kelime", f"{avg_words:.0f}")
                    
                    with col3:
                        html_count = sum(1 for r in results if r['has_html'])
                        st.metric("HTML Formatı", f"{html_count}/{len(results)}")
                    
                    # Detay tablosu
                    st.subheader("🔍 Detay Sonuçları")
                    for result in results:
                        st.write(f"**{result['prompt']}**: {result['length']} karakter, {result['words']} kelime")
                else:
                    st.error("Lütfen önce bir model seçin!")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.9em;'>
        <p>🤖 ShopifyGPT - Kendi AI Modeliniz | Ollama ile Güçlendirildi</p>
        <p>Mahir Yusuf Acan tarafından geliştirildi</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
