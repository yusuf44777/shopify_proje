import streamlit as st
import os
import time
import io
import subprocess
from dotenv import load_dotenv

# Try to import AI libraries with error handling
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

# Check if Ollama is available
def check_ollama():
    try:
        result = subprocess.run(['ollama', '--version'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

OLLAMA_AVAILABLE = check_ollama()

# Load environment variables
load_dotenv()

# Configure APIs
def configure_apis():
    if not OPENAI_AVAILABLE and not GEMINI_AVAILABLE and not OLLAMA_AVAILABLE:
        st.error("❌ Hiçbir AI kütüphanesi bulunamadı!")
        return False
    
    openai_api_key = st.session_state.get('openai_api_key', '')
    gemini_api_key = st.session_state.get('gemini_api_key', '')
    
    if openai_api_key and OPENAI_AVAILABLE:
        openai.api_key = openai_api_key
    
    if gemini_api_key and GEMINI_AVAILABLE:
        genai.configure(api_key=gemini_api_key)
    
    return True

# Get available Ollama models
def get_ollama_models():
    if not OLLAMA_AVAILABLE:
        return []
    
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            models = []
            for line in lines:
                if line.strip():
                    model_name = line.split()[0]  # İlk sütun model adı
                    models.append(model_name)
            return models
        else:
            return []
    except:
        return []

# Shopify-optimized prompt for product description generation
def get_shopify_prompt(keyword, language="English"):
    if language == "Türkçe":
        prompt = f"""
Sen Shopify ürün açıklamaları konusunda uzman bir e-ticaret metin yazarısın. "{keyword}" ile ilgili bir ürün için kapsamlı, SEO optimize edilmiş Türkçe ürün açıklaması oluştur.

KRİTİK YAZMA PRENSİPLERİ (Yüksek Dönüşüm Örneklerine Dayalı):
1. İLHAM VER & MOTİVE ET - Sadece açıklama yapma, müşterilerin başarı yolculuklarını hayal etmelerine yardım et
2. SPESİFİK & AÇIKLAYICI OL - Belirsiz dil kullanma, önemli olan kesin detayları kullan
3. MÜŞTERİ FAYDALARINA ODAKLAN - Bu ürün hayatlarına ne katacak?
4. ANAHTAR KELİME DOLDURMAKTAN KAÇIN - Doğal, bağlamsal anahtar kelime entegrasyonu kullan
5. DUYGUSAL BAĞLANTI KUR - Hedef kitleye hitap eden dil kullan
6. PRATİK TEŞVİKLER EKLİ - Kargo, garanti veya özel tekliflerden bahset

ETKİLİ VS ETKİSİZ YAKLAŞIM ÖRNEKLERİ:
✅ İYİ: "Fitness yolculuğunuzu kalıcı sonuçlar için tasarlanmış üst düzey ekipmanlarla yükseltin"
❌ KÖTÜ: "Ev ve spor salonu kullanımı için fitness ekipmanı satın alın"

✅ İYİ: "Doğa ile uyum içinde giyinmenizi sağlayan çevre dostu kıyafetlerle sürdürülebilir stile adım atın"
❌ KÖTÜ: "Çevre dostu kıyafetler mevcut. Sürdürülebilir ürünlerimize göz atın"

✅ İYİ: "Gerçek zamanlı olarak yazınızı düzelten kendi kendini bileyen mekanik kalem"
❌ KÖTÜ: "Mekanik kalem"

Gereksinimler:
1. Shopify'a uygun HTML formatında yaz
2. Uygun başlık hiyerarşisi kullan (h1, h2, h3, h4)
3. Eyleme geçmeye ilham veren etkileyici ürün özellik ve faydaları ekle
4. Call-to-action ve satın alma motivasyonu dahil et
5. SEO açısından anahtar kelimeyi doğal olarak entegre et
6. EMOJİ KULLANMA - Profesyonel görünüm için başlıklarda ve metinde emoji kullanmaktan kaçın

FORMAT:
```html
<h1>[Etkileyici Ana Başlık]</h1>
<p>[Motivasyonel açılış paragrafı]</p>

<h2>Neden Bu Ürünü Tercih Etmelisiniz?</h2>
<ul>
<li>[Ana fayda 1]</li>
<li>[Ana fayda 2]</li>
<li>[Ana fayda 3]</li>
</ul>

<h2>Öne Çıkan Özellikler</h2>
<ul>
<li>[Özellik 1 - Spesifik detay]</li>
<li>[Özellik 2 - Spesifik detay]</li>
<li>[Özellik 3 - Spesifik detay]</li>
</ul>

<h2>Müşteri Deneyimi</h2>
<p>[Ürünü kullanma deneyimi ve sonuçları]</p>

<h2>Hemen Sipariş Verin!</h2>
<p>[Satın alma motivasyonu ve aciliyet yaratma]</p>
```

Lütfen bu formata uygun, etkileyici ve profesyonel bir açıklama oluştur.
"""
    else:
        prompt = f"""
You are an expert Shopify product description writer specializing in high-converting e-commerce copy. Create a comprehensive, SEO-optimized English product description for a product related to "{keyword}".

CRITICAL WRITING PRINCIPLES (Based on High-Converting Examples):
1. INSPIRE & MOTIVATE - Don't just describe, help customers envision their success journey
2. BE SPECIFIC & DESCRIPTIVE - Avoid vague language, use concrete details that matter
3. FOCUS ON CUSTOMER BENEFITS - What will this product add to their lives?
4. AVOID KEYWORD STUFFING - Use natural, contextual keyword integration
5. CREATE EMOTIONAL CONNECTION - Use language that resonates with target audience
6. INCLUDE PRACTICAL INCENTIVES - Mention shipping, warranties, or special offers

EFFECTIVE vs INEFFECTIVE APPROACH EXAMPLES:
✅ GOOD: "Elevate your fitness journey with premium equipment designed for lasting results"
❌ BAD: "Buy fitness equipment for home and gym use"

✅ GOOD: "Step into sustainable style with eco-friendly clothing that lets you dress in harmony with nature"
❌ BAD: "Eco-friendly clothes available. Check out our sustainable products"

✅ GOOD: "Self-correcting mechanical pencil that fixes your writing in real-time"
❌ BAD: "Mechanical pencil"

Requirements:
1. Write in Shopify-compatible HTML format
2. Use proper heading hierarchy (h1, h2, h3, h4)
3. Include compelling product features and benefits that inspire action
4. Include call-to-action and purchase motivation
5. Integrate the keyword naturally for SEO

FORMAT:
```html
<h1>[Compelling Main Title]</h1>
<p>[Motivational opening paragraph]</p>

<h2>🎯 Why Choose This Product?</h2>
<ul>
<li>[Main benefit 1]</li>
<li>[Main benefit 2]</li>
<li>[Main benefit 3]</li>
</ul>

<h2>⭐ Key Features</h2>
<ul>
<li>[Feature 1 - Specific detail]</li>
<li>[Feature 2 - Specific detail]</li>
<li>[Feature 3 - Specific detail]</li>
</ul>

<h2>💫 Customer Experience</h2>
<p>[Product usage experience and results]</p>

<h2>🚀 Order Now!</h2>
<p>[Purchase motivation and urgency creation]</p>
```

Please create an engaging and professional description following this format.
"""
    return prompt

# Generate description with OpenAI
def generate_with_openai(keyword, model="gpt-4o", language="English"):
    if not OPENAI_AVAILABLE:
        return "Error: OpenAI library not available. Please install: pip install openai"
    
    if not st.session_state.get('openai_api_key'):
        return "Error: OpenAI API key not provided."
    
    try:
        prompt = get_shopify_prompt(keyword, language)
        
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert Shopify product description writer who creates compelling, SEO-optimized product descriptions that drive conversions."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating with OpenAI: {str(e)}"

# Generate description with Gemini
def generate_with_gemini(keyword, model="gemini-1.5-flash", language="English"):
    if not GEMINI_AVAILABLE:
        return "Error: Google Generative AI library not available. Please install: pip install google-generativeai"
    
    try:
        model_instance = genai.GenerativeModel(model)
        prompt = get_shopify_prompt(keyword, language)
        
        response = model_instance.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating with Gemini: {str(e)}"

# Generate description with Ollama
def generate_with_ollama(keyword, model="llama2", language="English"):
    if not OLLAMA_AVAILABLE:
        return "Error: Ollama not available. Please install Ollama first."
    
    try:
        prompt = get_shopify_prompt(keyword, language)
        
        # Ollama ile yanıt oluştur
        cmd = ['ollama', 'run', model, prompt]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
        else:
            return f"Error: {result.stderr if result.stderr else 'Model yanıt veremedi'}"
        
    except subprocess.TimeoutExpired:
        return "Error: Timeout - işlem çok uzun sürdü"
    except Exception as e:
        return f"Error generating with Ollama: {str(e)}"

# Enhanced word counter function
def enhanced_word_count(text):
    # Remove HTML tags for accurate word counting
    import re
    clean_text = re.sub(r'<[^>]+>', '', text)
    
    words = clean_text.split()
    return len(words)

# Enhanced character counter function  
def enhanced_char_count(text):
    # Remove HTML tags for accurate character counting
    import re
    clean_text = re.sub(r'<[^>]+>', '', text)
    
    return len(clean_text)

# Copy to clipboard function
def copy_to_clipboard(text):
    """JavaScript for copying text to clipboard"""
    escaped_text = text.replace('`', '\\`')
    st.markdown(
        f"""
        <script>
        function copyToClipboard() {{
            const textArea = document.createElement('textarea');
            textArea.value = `{escaped_text}`;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            alert('Metin panoya kopyalandı!');
        }}
        </script>
        """,
        unsafe_allow_html=True
    )

def main():
    # Set page config
    st.set_page_config(
        page_title="🛍️ Shopify GPT - Ürün Açıklama Üreticisi",
        page_icon="🛍️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better UI
    st.markdown("""
    <style>
    .main-title {
        color: #1e88e5;
        text-align: center;
        font-size: 3rem;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 3rem;
    }
    .feature-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stats-box {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #1e88e5;
        margin: 10px 0;
    }
    .result-container {
        background: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 20px 0;
    }
    .copy-button {
        background: linear-gradient(45deg, #FE6B8B 30%, #FF8E53 90%);
        border: none;
        border-radius: 3px;
        color: white;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        transition-duration: 0.4s;
    }
    .copy-button:hover {
        box-shadow: 0 12px 16px 0 rgba(0,0,0,0.24),0 17px 50px 0 rgba(0,0,0,0.19);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main title and subtitle
    st.markdown('<h1 class="main-title">🛍️ Shopify GPT</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Yapay Zeka Destekli Ürün Açıklama Üreticisi</p>', unsafe_allow_html=True)
    
    # Create two columns for better layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("⚙️ Ayarlar ve Yapılandırma")
        
        # Determine available providers
        available_providers = []
        if OPENAI_AVAILABLE:
            available_providers.append("OpenAI")
        if GEMINI_AVAILABLE:
            available_providers.append("Google Gemini")
        if OLLAMA_AVAILABLE:
            available_providers.append("Ollama")
        
        if not available_providers:
            st.error("❌ Hiçbir AI kütüphanesi bulunamadı! Lütfen gerekli kütüphaneleri yükleyin.")
            return
        
        api_provider = st.selectbox(
            "AI Sağlayıcısını Seçin:",
            available_providers,
            index=0
        )
        
        if api_provider == "OpenAI":
            st.markdown("**OpenAI Ayarları**")
            openai_api_key = st.text_input(
                "OpenAI API Anahtarı:",
                type="password",
                value=st.session_state.get('openai_api_key', ''),
                help="OpenAI API anahtarınızı girin"
            )
            
            if openai_api_key:
                st.session_state['openai_api_key'] = openai_api_key
                
            openai_model = st.selectbox(
                "OpenAI Model:",
                ["gpt-4o", "gpt-4", "gpt-3.5-turbo"],
                index=0,
                help="Kullanmak istediğiniz OpenAI modelini seçin"
            )
            st.session_state['openai_model'] = openai_model
            
        elif api_provider == "Google Gemini":
            st.markdown("**Google Gemini Ayarları**")
            gemini_api_key = st.text_input(
                "Gemini API Anahtarı:",
                type="password",
                value=st.session_state.get('gemini_api_key', ''),
                help="Google AI Studio'dan aldığınız API anahtarını girin"
            )
            
            if gemini_api_key:
                st.session_state['gemini_api_key'] = gemini_api_key
                
            gemini_model = st.selectbox(
                "Gemini Model:",
                ["gemini-1.5-flash", "gemini-1.5-pro"],
                index=0,
                help="Kullanmak istediğiniz Gemini modelini seçin"
            )
            st.session_state['gemini_model'] = gemini_model
        
        elif api_provider == "Ollama":
            st.markdown("**Ollama Ayarları**")
            ollama_models = get_ollama_models()
            
            if ollama_models:
                selected_ollama_model = st.selectbox(
                    "Ollama Model:",
                    ollama_models,
                    help="Yerel olarak kurulu Ollama modellerinden birini seçin"
                )
                st.session_state['ollama_model'] = selected_ollama_model
                
                st.success(f"✅ {len(ollama_models)} Ollama modeli bulundu")
                
                with st.expander("📋 Mevcut Modeller"):
                    for model in ollama_models:
                        st.write(f"• {model}")
            else:
                st.error("❌ Hiçbir Ollama modeli bulunamadı!")
                st.info("Model yüklemek için terminalde şu komutu çalıştırın: `ollama pull llama2`")
        
        # API status indicator
        st.markdown("---")
        st.subheader("📊 API Durumu")
        
        if api_provider == "OpenAI" and st.session_state.get('openai_api_key') and OPENAI_AVAILABLE:
            st.success("✅ OpenAI API hazır")
        elif api_provider == "Google Gemini" and st.session_state.get('gemini_api_key') and GEMINI_AVAILABLE:
            st.success("✅ Google Gemini API hazır")
        elif api_provider == "Ollama" and OLLAMA_AVAILABLE and ollama_models:
            st.success("✅ Ollama hazır")
        elif api_provider == "OpenAI" and not OPENAI_AVAILABLE:
            st.error("❌ OpenAI kütüphanesi yüklü değil")
        elif api_provider == "Google Gemini" and not GEMINI_AVAILABLE:
            st.error("❌ Google Generative AI kütüphanesi yüklü değil")
        elif api_provider == "Ollama" and not OLLAMA_AVAILABLE:
            st.error("❌ Ollama yüklü değil")
        else:
            st.warning("⚠️ API yapılandırması tamamlanmadı")
        
        # Input section
        st.markdown("---")
        st.subheader("📝 Ürün Bilgileri")
        
        keyword = st.text_input(
            "Ürün Anahtar Kelimesi:",
            placeholder="Örn: kablosuz kulaklık, yoga matı, kahve makinesi",
            help="Ürününüzü en iyi tanımlayan anahtar kelimeyi girin"
        )
        
        output_language = st.selectbox(
            "Çıktı Dili:",
            ["Türkçe", "English"],
            index=0,
            help="Ürün açıklamasının hangi dilde oluşturulacağını seçin"
        )
        
        # Generate button
        generate_button = st.button(
            "🚀 Açıklama Oluştur",
            disabled=not keyword or not (
                (api_provider == "OpenAI" and st.session_state.get('openai_api_key') and OPENAI_AVAILABLE) or
                (api_provider == "Google Gemini" and st.session_state.get('gemini_api_key') and GEMINI_AVAILABLE) or
                (api_provider == "Ollama" and OLLAMA_AVAILABLE and ollama_models)
            )
        )
        
        # Progress and generation
        if generate_button:
            if not keyword.strip():
                st.error("Lütfen bir ürün anahtar kelimesi girin.")
                return
            
            # Configure APIs
            if not configure_apis():
                st.error("❌ API yapılandırması başarısız!")
                return
            
            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                status_text.text("🔄 Ürün açıklaması oluşturuluyor...")
                progress_bar.progress(25)
                
                # Generate description based on selected provider
                if api_provider == "OpenAI":
                    progress_bar.progress(50)
                    result = generate_with_openai(keyword, st.session_state.get('openai_model', 'gpt-4o'), output_language)
                elif api_provider == "Google Gemini":
                    progress_bar.progress(50)
                    result = generate_with_gemini(keyword, st.session_state.get('gemini_model', 'gemini-1.5-flash'), output_language)
                else:  # Ollama
                    progress_bar.progress(50)
                    result = generate_with_ollama(keyword, st.session_state.get('ollama_model', 'llama2'), output_language)
                
                progress_bar.progress(75)
                
                if result and not result.startswith("Error"):
                    st.session_state['generated_description'] = result
                    st.session_state['current_keyword'] = keyword
                    st.session_state['selected_language'] = output_language
                    st.session_state['used_api'] = api_provider
                    progress_bar.progress(100)
                    status_text.empty()
                    if output_language == "Türkçe":
                        st.success("✅ Açıklama başarıyla oluşturuldu!")
                    else:
                        st.success("✅ Description generated successfully!")
                else:
                    st.error(f"❌ {result}")
                    
                progress_bar.empty()
                
            except Exception as e:
                st.error(f"❌ Bir hata oluştu: {str(e)}")
                progress_bar.empty()
                status_text.empty()
    
    with col2:
        st.header("📊 Oluşturulan Açıklama")
        
        if 'generated_description' in st.session_state:
            description = st.session_state['generated_description']
            keyword_used = st.session_state.get('current_keyword', 'ürün')
            language_used = st.session_state.get('selected_language', 'Türkçe')
            api_used = st.session_state.get('used_api', 'Unknown')
            
            # Display generated content in a nice container
            with st.container():
                st.markdown('<div class="result-container">', unsafe_allow_html=True)
                
                # Meta information
                col_meta1, col_meta2, col_meta3 = st.columns(3)
                with col_meta1:
                    st.metric("🎯 Anahtar Kelime", keyword_used)
                with col_meta2:
                    st.metric("🌍 Dil", language_used)
                with col_meta3:
                    st.metric("🤖 AI Provider", api_used)
                
                st.markdown("---")
                
                # Display the generated description
                st.markdown("### 📝 Ürün Açıklaması")
                st.markdown(description, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Analysis section
                st.markdown("---")
                st.subheader("📈 İçerik Analizi")
                
                col_stats1, col_stats2, col_stats3 = st.columns(3)
                
                with col_stats1:
                    word_count = enhanced_word_count(description)
                    st.markdown(f'<div class="stats-box"><strong>📊 Kelime Sayısı:</strong><br>{word_count} kelime</div>', unsafe_allow_html=True)
                
                with col_stats2:
                    char_count = enhanced_char_count(description)
                    st.markdown(f'<div class="stats-box"><strong>🔤 Karakter Sayısı:</strong><br>{char_count} karakter</div>', unsafe_allow_html=True)
                
                with col_stats3:
                    keyword_frequency = description.lower().count(keyword_used.lower())
                    st.markdown(f'<div class="stats-box"><strong>🎯 Anahtar Kelime Sıklığı:</strong><br>{keyword_frequency} kez</div>', unsafe_allow_html=True)
                
                # Copy and download section
                st.markdown("---")
                st.subheader("💾 İndirme ve Kopyalama")
                
                col_action1, col_action2 = st.columns(2)
                
                with col_action1:
                    # Copy to clipboard button
                    if st.button("📋 Panoya Kopyala", key="copy_btn"):
                        st.write("Metin seçili hale getirildi - Ctrl+C ile kopyalayabilirsiniz")
                        st.code(description, language="html")
                
                with col_action2:
                    # Download as file
                    timestamp = time.strftime("%Y%m%d_%H%M%S")
                    filename = f"shopify_description_{keyword_used.replace(' ', '_')}_{timestamp}.html"
                    
                    st.download_button(
                        label="💾 HTML Dosyası İndir",
                        data=description,
                        file_name=filename,
                        mime="text/html"
                    )
                
                # Raw HTML for copying
                with st.expander("📄 Ham HTML Kodu"):
                    st.code(description, language="html")
        
        else:
            # Default content when no description is generated
            st.info("👈 Bir ürün açıklaması oluşturmak için sol paneli kullanın")
            
            # Show features
            st.markdown("---")
            st.subheader("🌟 Özellikler")
            
            features = [
                "🤖 Çoklu AI Desteği (OpenAI, Gemini, Ollama)",
                "🎯 SEO Optimize Edilmiş İçerik",
                "🌍 Çok Dilli Destek (Türkçe/İngilizce)",
                "📊 İçerik Analizi ve İstatistikler",
                "💾 HTML İndirme ve Kopyalama",
                "⚡ Hızlı ve Kullanıcı Dostu Arayüz"
            ]
            
            for feature in features:
                st.markdown(f'<div class="feature-box">{feature}</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
