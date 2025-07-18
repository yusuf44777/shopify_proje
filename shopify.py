import streamlit as st
import os
import time
import io
from dotenv import load_dotenv

# Try to import AI libraries with error handling
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    st.error("⚠️ OpenAI library not found. Please install: pip install openai")

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    st.error("⚠️ Google Generative AI library not found. Please install: pip install google-generativeai")

# Load environment variables
load_dotenv()

# Configure APIs
def configure_apis():
    if not OPENAI_AVAILABLE and not GEMINI_AVAILABLE:
        st.error("❌ Hiçbir AI kütüphanesi bulunamadı!")
        return False
    
    openai_api_key = st.session_state.get('openai_api_key', '')
    gemini_api_key = st.session_state.get('gemini_api_key', '')
    
    if openai_api_key and OPENAI_AVAILABLE:
        openai.api_key = openai_api_key
    
    if gemini_api_key and GEMINI_AVAILABLE:
        genai.configure(api_key=gemini_api_key)
    
    return True

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
4. Duygusal tetikleyicilerle ikna edici eylem çağrısı öğeleri ekle
5. Doğal anahtar kelime entegrasyonu ile arama motorları için optimize et (ANAHTAR KELİME DOLDURMA YOK)
6. Shopify'ın en iyi uygulamalarını takip et
7. Uygun olduğunda sosyal kanıt öğeleri ve güven sinyalleri ekle
8. Net değer önermeleriyle dönüşüm odaklı ve müşteri merkezli yap

Yanıtını şu yapıyla oluştur:
- Ürün Başlığı (h1) - İlham verici ve spesifik yap
- Etkileyici Açılış Bildirimi (p) - Müşteriyi hemen yakala
- Ana Özellikler ve Faydalar (h2) - Dönüşüm ve sonuçlara odaklan
- Ürün Detayları (h3) - Spesifik ve açıklayıcı ol
- Ürün Boyutları (h3) - HER ZAMAN hem inç hem santimetre cinsinden gerçekçi boyutlar ekle
  * TABLO formatında düzenle, liste değil
  * Örnek format:
    <table style="width:100%; border-collapse: collapse; margin: 10px 0;">
    <tr style="background-color: #f8f9fa;">
      <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Boyut</th>
      <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">İnç</th>
      <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Santimetre</th>
    </tr>
    <tr>
      <td style="border: 1px solid #ddd; padding: 8px;">Uzunluk</td>
      <td style="border: 1px solid #ddd; padding: 8px;">12"</td>
      <td style="border: 1px solid #ddd; padding: 8px;">30,5 cm</td>
    </tr>
    </table>
  * Uzunluk, Genişlik, Yükseklik, Derinlik, Çap gibi ilgili boyutları ekle
  * Ürün kategorisi için gerçekçi boyutlar yap
- Teknik Özellikler (h4 gerekirse) - İlgili teknik detayları ekle
- Bakım Talimatları veya Kullanım Kılavuzları (h3) - Pratik katma değer bilgisi
- Bu Ürünü Neden Seçmelisiniz (h2) - Farklılaşma ve benzersiz değer
- Müşteri Faydaları ve Yaşam Tarzı Etkisi (h3) - Başarı resmini çiz
- Eylem Çağrısı Bölümü - Aciliyet ve arzu yarat

Kılavuzlar:
- Eyleme geçmeye ilham veren duygusal tetikleyiciler ve güç kelimeleri kullan
- Sadece özellikler değil faydalar ve dönüşüme odaklan
- Müşterilerin ilişki kurabileceği yaşam tarzı ve kullanım senaryolarını ekle
- Madde işaretleri ve kısa, etkili paragraflarla taranabilir yap
- Net hiyerarşiyle mobil okuma için optimize et
- Güven sinyalleri, garantiler ve pratik teşvikler ekle (ücretsiz kargo, garantiler vb.)
- Dönüşümleri artıran ve arzu yaratan ikna edici dil kullan
- Spesifik ve açıklayıcı ol - genel ifadelerden kaçın
- Müşterilerin ürününle başarı yolculuklarını hayal etmelerine yardım et
- Pratik değer verirken duygusal bağlantı kur
- HER ZAMAN hem inç hem santimetre cinsinden gerçekçi ürün boyutları ekle
- Boyutları kolay tarama için düzenli TABLO formatında sun, liste değil
- Boyutları ürün kategorisine uygun ve gerçekçi yap

"{keyword}" kategorisinde premium kaliteli bir ürün satıyormuş gibi açıklama yaz. Etkileyici, bilgilendirici, dönüşüm optimize edilmiş ve ilham verici yap. Bu ürünün müşterinin hayatını nasıl dönüştüreceğine veya spesifik problemlerini nasıl çözeceğine odaklan.

Sadece HTML içeriğini çıktı ver, ek açıklama veya markdown formatlaması olmadan.
"""
    else:  # English
        prompt = f"""
You are an expert e-commerce copywriter specializing in Shopify product descriptions. Create a comprehensive, SEO-optimized product description for a product related to "{keyword}".

CRITICAL WRITING PRINCIPLES (Based on High-Converting Examples):
1. INSPIRE & MOTIVATE - Don't just describe, help customers envision their success journey
2. BE SPECIFIC & DESCRIPTIVE - Avoid vague language, use precise details that matter
3. FOCUS ON CUSTOMER BENEFITS - What will this product do for their life?
4. AVOID KEYWORD STUFFING - Use natural, contextual keyword integration
5. CREATE EMOTIONAL CONNECTION - Use language that resonates with target audience
6. INCLUDE PRACTICAL INCENTIVES - Mention shipping, guarantees, or special offers when relevant

EXAMPLES OF EFFECTIVE VS INEFFECTIVE APPROACHES:
✅ GOOD: "Elevate your fitness journey with top-tier equipment designed for lasting results"
❌ BAD: "Buy fitness equipment for home and gym use"

✅ GOOD: "Step into sustainable style with eco-friendly clothing that lets you dress in harmony with nature"
❌ BAD: "Eco-friendly clothing available. Browse our sustainable products"

✅ GOOD: "Self-sharpening mechanical pencil that autocorrects your penmanship in real time"
❌ BAD: "Mechanical pencil"

Requirements:
1. Write in HTML format suitable for Shopify
2. Use proper heading hierarchy (h1, h2, h3, h4)
3. Include compelling product features and benefits that inspire action
4. Add persuasive call-to-action elements with emotional triggers
5. Optimize for search engines with natural keyword integration (NO keyword stuffing)
6. Follow Shopify's best practices for product descriptions
7. Include social proof elements and trust signals when appropriate
8. Make it conversion-focused and customer-centric with clear value propositions

Structure your response with:
- Product Title (h1) - Make it inspiring and specific
- Compelling Opening Statement (p) - Hook the customer immediately
- Key Features & Benefits (h2) - Focus on transformation and results
- Product Details (h3) - Be specific and descriptive
- Product Dimensions (h3) - ALWAYS include realistic dimensions in BOTH inches and centimeters
  * Format as HTML TABLE, not list
  * Example format:
    <table style="width:100%; border-collapse: collapse; margin: 10px 0;">
    <tr style="background-color: #f8f9fa;">
      <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Dimension</th>
      <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Inches</th>
      <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Centimeters</th>
    </tr>
    <tr>
      <td style="border: 1px solid #ddd; padding: 8px;">Length</td>
      <td style="border: 1px solid #ddd; padding: 8px;">12"</td>
      <td style="border: 1px solid #ddd; padding: 8px;">30.5 cm</td>
    </tr>
    </table>
  * Include relevant dimensions like: Length, Width, Height, Depth, Diameter, etc.
  * Make dimensions realistic for the product category
- Specifications (h4 if needed) - Include relevant technical details
- Care Instructions or Usage Guidelines (h3) - Practical value-add information
- Why Choose This Product (h2) - Differentiation and unique value
- Customer Benefits & Lifestyle Impact (h3) - Paint the success picture
- Call-to-Action Section - Create urgency and desire

Guidelines:
- Use emotional triggers and power words that inspire action
- Focus on benefits and transformation over mere features
- Include lifestyle and usage scenarios that customers can relate to
- Make it scannable with bullet points and short, impactful paragraphs
- Optimize for mobile reading with clear hierarchy
- Include trust signals, guarantees, and practical incentives (free shipping, warranties, etc.)
- Use persuasive language that drives conversions and builds desire
- Be specific and descriptive - avoid generic statements
- Help customers envision their success journey with your product
- Create emotional connection while providing practical value
- ALWAYS include realistic product dimensions in both inches and centimeters
- Present dimensions in a clear, organized TABLE format for easy scanning, not lists
- Make dimensions appropriate for the product category and realistic

Write the description as if you're selling a premium quality product in the "{keyword}" category. Make it engaging, informative, conversion-optimized, and inspirational. Focus on how this product will transform the customer's life or solve their specific problems.

Output only the HTML content without any additional explanation or markdown formatting.
"""
    
    return prompt

# Generate description with OpenAI
def generate_with_openai(keyword, model="gpt-4o", language="English"):
    if not OPENAI_AVAILABLE:
        return "Error: OpenAI library not available. Please install: pip install openai"
    
    try:
        client = openai.OpenAI(api_key=st.session_state.get('openai_api_key'))
        prompt = get_shopify_prompt(keyword, language)
        
        system_message = "You are an expert e-commerce copywriter specializing in Shopify product descriptions. Always respond with clean HTML code that follows Shopify best practices."
        if language == "Türkçe":
            system_message = "Sen Shopify ürün açıklamaları konusunda uzman bir e-ticaret metin yazarısın. Her zaman Shopify'ın en iyi uygulamalarını takip eden temiz HTML kodu ile yanıtla."
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_message},
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

# Download HTML file
def create_download_link(content, filename):
    """Create a download link for the generated content"""
    return st.download_button(
        label="📥 HTML Dosyasını İndir",
        data=content,
        file_name=filename,
        mime="text/html",
        key="download_btn"
    )

# Main Streamlit app
def main():
    st.set_page_config(
        page_title="Shopify Ürün Açıklama Üreticisi",
        page_icon="🛍️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better styling
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
    .api-config {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .result-container {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e6e6e6;
        margin-top: 1rem;
    }
    .stTextArea textarea {
        background-color: #f8f9fa;
        border: 2px solid #e9ecef;
        border-radius: 5px;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🛍️ Shopify Ürün Açıklama Üreticisi</h1>
        <p>Shopify mağazanız için etkileyici, SEO optimize edilmiş ürün açıklamaları oluşturun</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for API configuration
    with st.sidebar:
        st.header("🔧 API Yapılandırması")
        
        # API Selection
        available_providers = []
        if OPENAI_AVAILABLE:
            available_providers.append("OpenAI")
        if GEMINI_AVAILABLE:
            available_providers.append("Google Gemini")
        
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
            st.session_state['openai_api_key'] = openai_api_key
            
            openai_model = st.selectbox(
                "Model:",
                ["gpt-4o", "gpt-4o-mini", "gpt-4", "gpt-3.5-turbo"],
                index=0
            )
            st.session_state['openai_model'] = openai_model
            
        else:  # Gemini
            st.markdown("**Google Gemini Ayarları**")
            gemini_api_key = st.text_input(
                "Gemini API Anahtarı:",
                type="password",
                value=st.session_state.get('gemini_api_key', ''),
                help="Google Gemini API anahtarınızı girin"
            )
            st.session_state['gemini_api_key'] = gemini_api_key
            
            gemini_model = st.selectbox(
                "Model:",
                ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"],
                index=0
            )
            st.session_state['gemini_model'] = gemini_model
        
        # Configuration status
        if api_provider == "OpenAI" and st.session_state.get('openai_api_key') and OPENAI_AVAILABLE:
            st.success("✅ OpenAI API yapılandırıldı")
        elif api_provider == "Google Gemini" and st.session_state.get('gemini_api_key') and GEMINI_AVAILABLE:
            st.success("✅ Gemini API yapılandırıldı")
        elif api_provider == "OpenAI" and not OPENAI_AVAILABLE:
            st.error("❌ OpenAI kütüphanesi bulunamadı")
        elif api_provider == "Google Gemini" and not GEMINI_AVAILABLE:
            st.error("❌ Gemini kütüphanesi bulunamadı")
        else:
            st.warning("⚠️ Lütfen API anahtarınızı yapılandırın")
        
        st.markdown("---")
        
        # Tips section
        st.markdown("""
        **💡 Daha iyi sonuçlar için ipuçları:**
        - Spesifik ürün anahtar kelimeleri kullanın
        - Marka adlarını dahil edin
        - Açıklayıcı olun (örn: "su geçirmez yürüyüş ayakkabısı" vs "ayakkabı")
        - Hedef kitlenizi düşünün
        """)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📝 Ürün Bilgileri")
        
        # Language selection
        output_language = st.selectbox(
            "Çıktı Dili:",
            ["English", "Türkçe"],
            index=0,
            help="Ürün açıklamasının hangi dilde oluşturulacağını seçin"
        )
        
        # Keyword input
        keyword = st.text_input(
            "Ürün Anahtar Kelimesi:",
            placeholder="örn: kablosuz bluetooth kulaklık, organik cilt bakım serumu, vintage deri ceket",
            help="Açıklama oluşturmak istediğiniz ana anahtar kelime veya ürün türünü girin"
        )
        
        # Generate button
        generate_button = st.button(
            "🚀 Açıklama Oluştur",
            type="primary",
            disabled=not keyword or not (
                (api_provider == "OpenAI" and st.session_state.get('openai_api_key') and OPENAI_AVAILABLE) or
                (api_provider == "Google Gemini" and st.session_state.get('gemini_api_key') and GEMINI_AVAILABLE)
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
                else:
                    progress_bar.progress(50)
                    result = generate_with_gemini(keyword, st.session_state.get('gemini_model', 'gemini-1.5-flash'), output_language)
                
                progress_bar.progress(75)
                
                if result and not result.startswith("Error"):
                    st.session_state['generated_description'] = result
                    st.session_state['current_keyword'] = keyword
                    st.session_state['selected_language'] = output_language
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
            selected_language = st.session_state.get('selected_language', 'English')
            
            # Show language indicator
            if selected_language == "Türkçe":
                st.info(f"🇹🇷 Türkçe açıklama oluşturuldu: {keyword_used}")
            else:
                st.info(f"🇺🇸 English description generated: {keyword_used}")
            
            # Display tabs
            tab1, tab2, tab3 = st.tabs(["📝 Düzenle", "👁️ Önizleme", "📋 Kopyala"])
            
            with tab1:
                # Editable text area
                edited_description = st.text_area(
                    "Açıklamanızı düzenleyin:",
                    value=description,
                    height=400,
                    help="Oluşturulan açıklamayı burada düzenleyebilirsiniz"
                )
                
                # Update button
                if st.button("💾 Açıklamayı Güncelle"):
                    st.session_state['generated_description'] = edited_description
                    st.success("Açıklama güncellendi!")
                    st.rerun()
            
            with tab2:
                # HTML preview
                st.markdown("**HTML Önizlemesi:**")
                try:
                    st.components.v1.html(
                        f"<div style='padding: 20px; border: 1px solid #ddd; border-radius: 5px;'>{description}</div>",
                        height=400,
                        scrolling=True
                    )
                except:
                    st.code(description, language='html')
            
            with tab3:
                # Copy section
                st.markdown("**HTML Kodunu Kopyala:**")
                st.code(description, language='html')
                
                # Download functionality
                if selected_language == "Türkçe":
                    filename = f"shopify_aciklama_{keyword_used.replace(' ', '_')}_turkce.html"
                else:
                    filename = f"shopify_description_{keyword_used.replace(' ', '_')}_english.html"
                create_download_link(description, filename)
                
                # Copy to clipboard info
                st.info("💡 Yukarıdaki kodu kopyalamak için Ctrl+C (Mac'te Cmd+C) kullanın")
        
        else:
            st.info("👆 Bir anahtar kelime girin ve başlamak için 'Açıklama Oluştur' butonuna tıklayın!")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.9em;'>
        <p>🛍️ Shopify Ürün Açıklama Üreticisi | Powered by Mahir Yusuf Acan | Streamlit ile Geliştirildi</p>
        <p>E-ticaret ürünleriniz için etkileyici, SEO optimize edilmiş açıklamalar oluşturun</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()