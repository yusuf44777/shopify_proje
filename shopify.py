import streamlit as st
import openai
import google.generativeai as genai
import os
from dotenv import load_dotenv
import time
import io

# Load environment variables
load_dotenv()

# Configure APIs
def configure_apis():
    openai_api_key = st.session_state.get('openai_api_key', '')
    gemini_api_key = st.session_state.get('gemini_api_key', '')
    
    if openai_api_key:
        openai.api_key = openai_api_key
    
    if gemini_api_key:
        genai.configure(api_key=gemini_api_key)

# Shopify-optimized prompt for product description generation
def get_shopify_prompt(keyword):
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
  * Format as clean HTML list with both measurements
  * Example: <li>Length: 12 inches (30.5 cm)</li>
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

Write the description as if you're selling a premium quality product in the "{keyword}" category. Make it engaging, informative, conversion-optimized, and inspirational. Focus on how this product will transform the customer's life or solve their specific problems.

Output only the HTML content without any additional explanation or markdown formatting.
"""
    return prompt

# Generate description with OpenAI
def generate_with_openai(keyword, model="gpt-4o"):
    try:
        client = openai.OpenAI(api_key=st.session_state.get('openai_api_key'))
        prompt = get_shopify_prompt(keyword)
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert e-commerce copywriter specializing in Shopify product descriptions. Always respond with clean HTML code that follows Shopify best practices."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating with OpenAI: {str(e)}"

# Generate description with Gemini
def generate_with_gemini(keyword, model="gemini-1.5-flash"):
    try:
        model_instance = genai.GenerativeModel(model)
        prompt = get_shopify_prompt(keyword)
        
        response = model_instance.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating with Gemini: {str(e)}"

# Download HTML file
def create_download_link(content, filename):
    """Create a download link for the generated content"""
    return st.download_button(
        label="📥 Download HTML File",
        data=content,
        file_name=filename,
        mime="text/html",
        key="download_btn"
    )

# Main Streamlit app
def main():
    st.set_page_config(
        page_title="Shopify Description Generator",
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
        <h1>🛍️ Shopify Product Description Generator</h1>
        <p>Generate compelling, SEO-optimized product descriptions for your Shopify store</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for API configuration
    with st.sidebar:
        st.header("🔧 API Configuration")
        
        # API Selection
        api_provider = st.selectbox(
            "Choose AI Provider:",
            ["OpenAI", "Google Gemini"],
            index=0
        )
        
        if api_provider == "OpenAI":
            st.markdown("**OpenAI Settings**")
            openai_api_key = st.text_input(
                "OpenAI API Key:",
                type="password",
                value=st.session_state.get('openai_api_key', ''),
                help="Enter your OpenAI API key"
            )
            st.session_state['openai_api_key'] = openai_api_key
            
            openai_model = st.selectbox(
                "Model:",
                ["gpt-4o", "gpt-4o-mini", "gpt-4", "gpt-3.5-turbo"],
                index=0
            )
            st.session_state['openai_model'] = openai_model
            
        else:  # Gemini
            st.markdown("**Google Gemini Settings**")
            gemini_api_key = st.text_input(
                "Gemini API Key:",
                type="password",
                value=st.session_state.get('gemini_api_key', ''),
                help="Enter your Google Gemini API key"
            )
            st.session_state['gemini_api_key'] = gemini_api_key
            
            gemini_model = st.selectbox(
                "Model:",
                ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"],
                index=0
            )
            st.session_state['gemini_model'] = gemini_model
        
        # Configuration status
        if api_provider == "OpenAI" and st.session_state.get('openai_api_key'):
            st.success("✅ OpenAI API configured")
        elif api_provider == "Google Gemini" and st.session_state.get('gemini_api_key'):
            st.success("✅ Gemini API configured")
        else:
            st.warning("⚠️ Please configure your API key")
        
        st.markdown("---")
        
        # Tips section
        st.markdown("""
        **💡 Tips for better results:**
        - Use specific product keywords
        - Include brand names when relevant
        - Be descriptive (e.g., "waterproof hiking boots" vs "boots")
        - Consider your target audience
        """)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📝 Product Information")
        
        # Keyword input
        keyword = st.text_input(
            "Product Keyword:",
            placeholder="e.g., wireless bluetooth headphones, organic skincare serum, vintage leather jacket",
            help="Enter the main keyword or product type you want to create a description for"
        )
        
        # Generate button
        generate_button = st.button(
            "🚀 Generate Description",
            type="primary",
            disabled=not keyword or not (
                (api_provider == "OpenAI" and st.session_state.get('openai_api_key')) or
                (api_provider == "Google Gemini" and st.session_state.get('gemini_api_key'))
            )
        )
        
        # Progress and generation
        if generate_button:
            if not keyword.strip():
                st.error("Please enter a product keyword.")
                return
            
            # Configure APIs
            configure_apis()
            
            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                status_text.text("🔄 Generating product description...")
                progress_bar.progress(25)
                
                # Generate description based on selected provider
                if api_provider == "OpenAI":
                    progress_bar.progress(50)
                    result = generate_with_openai(keyword, st.session_state.get('openai_model', 'gpt-4o'))
                else:
                    progress_bar.progress(50)
                    result = generate_with_gemini(keyword, st.session_state.get('gemini_model', 'gemini-1.5-flash'))
                
                progress_bar.progress(75)
                
                if result and not result.startswith("Error"):
                    st.session_state['generated_description'] = result
                    st.session_state['current_keyword'] = keyword
                    progress_bar.progress(100)
                    status_text.empty()
                    st.success("✅ Description generated successfully!")
                else:
                    st.error(f"❌ {result}")
                    
                progress_bar.empty()
                
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                progress_bar.empty()
                status_text.empty()
    
    with col2:
        st.header("📊 Generated Description")
        
        if 'generated_description' in st.session_state:
            description = st.session_state['generated_description']
            keyword_used = st.session_state.get('current_keyword', 'product')
            
            # Display tabs
            tab1, tab2, tab3 = st.tabs(["📝 Edit", "👁️ Preview", "📋 Copy"])
            
            with tab1:
                # Editable text area
                edited_description = st.text_area(
                    "Edit your description:",
                    value=description,
                    height=400,
                    help="You can edit the generated description here"
                )
                
                # Update button
                if st.button("💾 Update Description"):
                    st.session_state['generated_description'] = edited_description
                    st.success("Description updated!")
                    st.rerun()
            
            with tab2:
                # HTML preview
                st.markdown("**HTML Preview:**")
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
                st.markdown("**Copy HTML Code:**")
                st.code(description, language='html')
                
                # Download functionality
                filename = f"shopify_description_{keyword_used.replace(' ', '_')}.html"
                create_download_link(description, filename)
                
                # Copy to clipboard info
                st.info("💡 Use Ctrl+C (Cmd+C on Mac) to copy the code above")
        
        else:
            st.info("👆 Enter a keyword and click 'Generate Description' to get started!")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.9em;'>
        <p>🛍️ Shopify Product Description Generator | Powered by AI | Built with Streamlit</p>
        <p>Generate compelling, SEO-optimized descriptions for your e-commerce products</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()