import requests
import json
import time
import csv
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pandas as pd
from datetime import datetime
import subprocess

class ShopifyDataCollector:
    def __init__(self):
        self.data = []
        self.scraped_urls = set()
        self.output_dir = "shopify_training_data"
        self.ensure_output_dir()
        
        # Selenium setup
        self.setup_selenium()
        
        # AI model configuration
        self.available_models = self.get_available_ollama_models()
        self.selected_ai_model = None
        
        # User agents for rotation
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        ]
    
    def ensure_output_dir(self):
        """Çıktı dizinini oluştur"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def get_available_ollama_models(self):
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
                print(f"✅ {len(models)} Ollama modeli bulundu: {models}")
                return models
            else:
                print("⚠️ Ollama modelleri listelenemedi")
                return []
        except FileNotFoundError:
            print("⚠️ Ollama kurulu değil")
            return []
        except Exception as e:
            print(f"⚠️ Ollama model listesi alınırken hata: {e}")
            return []
    
    def select_ai_model(self):
        """Kullanıcıdan AI model seçimi al"""
        print("\n🤖 AI Model Seçimi")
        print("=" * 40)
        
        if not self.available_models:
            print("❌ Hiçbir Ollama modeli bulunamadı!")
            print("💡 İpucu: 'ollama pull llama2' komutu ile model indirebilirsiniz")
            return None
        
        print("Mevcut Ollama modelleri:")
        for i, model in enumerate(self.available_models, 1):
            print(f"{i}. {model}")
        
        print(f"{len(self.available_models) + 1}. AI kullanmadan devam et")
        
        while True:
            try:
                choice = input(f"\nSeçiminiz (1-{len(self.available_models) + 1}): ").strip()
                
                if choice == str(len(self.available_models) + 1):
                    print("ℹ️ AI model kullanılmadan devam ediliyor")
                    return None
                
                choice_num = int(choice)
                if 1 <= choice_num <= len(self.available_models):
                    selected_model = self.available_models[choice_num - 1]
                    print(f"✅ Seçilen model: {selected_model}")
                    return selected_model
                else:
                    print("❌ Geçersiz seçim!")
                    
            except ValueError:
                print("❌ Lütfen sayı girin!")
            except KeyboardInterrupt:
                print("\n⚠️ İşlem iptal edildi")
                return None
    
    def generate_with_ollama(self, prompt, model_name):
        """Ollama ile içerik oluştur"""
        if not model_name:
            return None
        
        try:
            # Ollama komutu ile içerik oluştur
            cmd = ['ollama', 'run', model_name, prompt]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
            else:
                print(f"⚠️ Ollama yanıt hatası: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            print("⚠️ Ollama zaman aşımı")
            return None
        except Exception as e:
            print(f"⚠️ Ollama hatası: {e}")
            return None
    
    def enhance_product_data_with_ai(self, product_data):
        """Ürün verisini AI ile zenginleştir"""
        if not self.selected_ai_model or not product_data:
            return product_data
        
        try:
            # AI ile ek açıklama oluştur
            prompt = f"""Create a brief, compelling product description enhancement for:
Title: {product_data.get('title', '')}
Category: {product_data.get('category', '')}
Features: {', '.join(product_data.get('features', [])[:3])}

Provide only the enhanced description, no additional text."""
            
            ai_enhancement = self.generate_with_ollama(prompt, self.selected_ai_model)
            
            if ai_enhancement:
                product_data['ai_enhanced_description'] = ai_enhancement
                product_data['ai_model_used'] = self.selected_ai_model
                print(f"🤖 AI ile zenginleştirildi: {self.selected_ai_model}")
            
        except Exception as e:
            print(f"⚠️ AI zenginleştirme hatası: {e}")
        
        return product_data
    
    def setup_selenium(self):
        """Selenium WebDriver'ı ayarla"""
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument(f"--user-agent={random.choice(self.user_agents)}")
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.implicitly_wait(10)
            print("✅ Selenium WebDriver başarıyla ayarlandı")
        except Exception as e:
            print(f"⚠️ Selenium ayarlanamadı: {e}")
            self.driver = None
    
    def scrape_shopify_product(self, url):
        """Shopify ürün sayfasından veri çek"""
        try:
            if self.driver:
                self.driver.get(url)
                time.sleep(random.uniform(2, 5))
                
                # Ürün başlığı
                title = ""
                try:
                    title_element = self.driver.find_element(By.CSS_SELECTOR, "h1, .product-title, [class*='title'], [class*='name']")
                    title = title_element.text.strip()
                except:
                    pass
                
                # Ürün açıklaması
                description = ""
                try:
                    desc_selectors = [
                        ".product-description",
                        ".product-content",
                        "[class*='description']",
                        ".rte",
                        ".product-single__description"
                    ]
                    for selector in desc_selectors:
                        try:
                            desc_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                            description = desc_element.get_attribute('innerHTML')
                            if description:
                                break
                        except:
                            continue
                except:
                    pass
                
                # Fiyat
                price = ""
                try:
                    price_selectors = [
                        ".price",
                        ".product-price",
                        "[class*='price']",
                        ".money"
                    ]
                    for selector in price_selectors:
                        try:
                            price_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                            price = price_element.text.strip()
                            if price:
                                break
                        except:
                            continue
                except:
                    pass
                
                # Kategori/koleksiyon
                category = ""
                try:
                    breadcrumb = self.driver.find_elements(By.CSS_SELECTOR, ".breadcrumb a, nav a")
                    if breadcrumb:
                        category = " > ".join([b.text.strip() for b in breadcrumb if b.text.strip()])
                except:
                    pass
                
                # Ürün özellikleri
                features = []
                try:
                    feature_elements = self.driver.find_elements(By.CSS_SELECTOR, ".product-features li, .product-details li, ul li")
                    features = [f.text.strip() for f in feature_elements if f.text.strip()]
                except:
                    pass
                
                if title and description:
                    product_data = {
                        'url': url,
                        'title': title,
                        'description': self.clean_html(description),
                        'price': price,
                        'category': category,
                        'features': features,
                        'scraped_at': datetime.now().isoformat()
                    }
                    
                    # AI ile zenginleştir
                    product_data = self.enhance_product_data_with_ai(product_data)
                    
                    return product_data
                    
        except Exception as e:
            print(f"❌ Hata oluştu {url}: {e}")
        
        return None
    
    def clean_html(self, html_content):
        """HTML içeriğini temizle"""
        if not html_content:
            return ""
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Script ve style etiketlerini kaldır
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Metni al ve temizle
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
    
    def find_shopify_sites(self, keywords):
        """Shopify sitelerini bul"""
        shopify_sites = []
        
        # Bilinen Shopify mağazaları
        known_shopify_domains = [
            "gymshark.com",
            "allbirds.com",
            "bombas.com",
            "mvmt.com",
            "colourpop.com",
            "fashionnova.com",
            "kylie-cosmetics.com",
            "jeffreestarcosmetics.com",
            "morphe.com",
            "haus-labs.com"
        ]
        
        # Google aramalarından Shopify siteleri bul
        for keyword in keywords:
            try:
                search_url = f"https://www.google.com/search?q={keyword}+site:myshopify.com"
                headers = {'User-Agent': random.choice(self.user_agents)}
                response = requests.get(search_url, headers=headers)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    links = soup.find_all('a', href=True)
                    
                    for link in links:
                        href = link['href']
                        if 'myshopify.com' in href or any(domain in href for domain in known_shopify_domains):
                            if href.startswith('/url?q='):
                                href = href.split('/url?q=')[1].split('&')[0]
                            if href not in shopify_sites:
                                shopify_sites.append(href)
                
                time.sleep(random.uniform(3, 7))  # Rate limiting
                
            except Exception as e:
                print(f"❌ Arama hatası {keyword}: {e}")
        
        return shopify_sites
    
    def scrape_product_urls_from_site(self, site_url):
        """Bir siteden ürün URL'lerini çek"""
        product_urls = []
        
        try:
            if self.driver:
                self.driver.get(site_url)
                time.sleep(random.uniform(3, 6))
                
                # Ürün linklerini bul
                product_selectors = [
                    "a[href*='/products/']",
                    "a[href*='/product/']",
                    ".product-item a",
                    ".product-card a",
                    ".grid-product a"
                ]
                
                for selector in product_selectors:
                    try:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        for element in elements:
                            href = element.get_attribute('href')
                            if href and ('/products/' in href or '/product/' in href):
                                full_url = urljoin(site_url, href)
                                if full_url not in product_urls:
                                    product_urls.append(full_url)
                    except:
                        continue
                
                # Koleksiyon sayfalarını da kontrol et
                try:
                    collection_links = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='/collections/']")
                    for link in collection_links[:5]:  # İlk 5 koleksiyon
                        try:
                            collection_url = link.get_attribute('href')
                            if collection_url:
                                self.driver.get(collection_url)
                                time.sleep(2)
                                
                                collection_products = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='/products/']")
                                for product in collection_products:
                                    href = product.get_attribute('href')
                                    if href:
                                        full_url = urljoin(site_url, href)
                                        if full_url not in product_urls:
                                            product_urls.append(full_url)
                        except:
                            continue
                except:
                    pass
                    
        except Exception as e:
            print(f"❌ Site tarama hatası {site_url}: {e}")
        
        return product_urls
    
    def collect_training_data(self, keywords, max_products_per_keyword=50):
        """Eğitim verisi topla"""
        print("🚀 Shopify eğitim verisi toplama başlıyor...")
        
        # AI model seçimi
        self.selected_ai_model = self.select_ai_model()
        
        # Shopify sitelerini bul
        print("🔍 Shopify siteleri aranıyor...")
        shopify_sites = self.find_shopify_sites(keywords)
        print(f"✅ {len(shopify_sites)} Shopify sitesi bulundu")
        
        total_collected = 0
        
        for site in shopify_sites[:10]:  # İlk 10 site
            try:
                print(f"📋 Site taranıyor: {site}")
                product_urls = self.scrape_product_urls_from_site(site)
                print(f"✅ {len(product_urls)} ürün URL'si bulundu")
                
                # Her siteden maksimum ürün sayısını sınırla
                for url in product_urls[:max_products_per_keyword]:
                    if url in self.scraped_urls:
                        continue
                    
                    print(f"📝 Ürün verisi çekiliyor: {url[:50]}...")
                    product_data = self.scrape_shopify_product(url)
                    
                    if product_data:
                        self.data.append(product_data)
                        self.scraped_urls.add(url)
                        total_collected += 1
                        print(f"✅ Veri toplandı ({total_collected} toplam)")
                        
                        # Her 10 üründe bir kaydet
                        if total_collected % 10 == 0:
                            self.save_data()
                    
                    # Rate limiting
                    time.sleep(random.uniform(2, 5))
                    
            except Exception as e:
                print(f"❌ Site işleme hatası {site}: {e}")
        
        print(f"🎉 Toplanan veri sayısı: {total_collected}")
        self.save_data()
        self.close()
        
        return total_collected
    
    def save_data(self):
        """Toplanan veriyi kaydet"""
        if not self.data:
            return
        
        # JSON formatında kaydet
        json_file = os.path.join(self.output_dir, f"shopify_products_{datetime.now().strftime('%Y%m%d_%H%M')}.json")
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        
        # CSV formatında kaydet
        csv_file = os.path.join(self.output_dir, f"shopify_products_{datetime.now().strftime('%Y%m%d_%H%M')}.csv")
        if self.data:
            df = pd.DataFrame(self.data)
            df.to_csv(csv_file, index=False, encoding='utf-8')
        
        print(f"💾 Veri kaydedildi: {len(self.data)} kayıt")
    
    def close(self):
        """Kaynakları temizle"""
        if self.driver:
            self.driver.quit()

def main():
    """Ana fonksiyon"""
    collector = ShopifyDataCollector()
    
    # Anahtar kelimeler - kategoriler
    keywords = [
        "fashion+clothing",
        "beauty+cosmetics", 
        "electronics+gadgets",
        "home+decor",
        "fitness+sports",
        "jewelry+accessories",
        "kitchen+appliances",
        "baby+kids",
        "books+media",
        "toys+games"
    ]
    
    try:
        total_collected = collector.collect_training_data(keywords, max_products_per_keyword=30)
        print(f"🎉 Veri toplama tamamlandı! Toplam: {total_collected} ürün")
    except KeyboardInterrupt:
        print("\n⚠️ İşlem kullanıcı tarafından durduruldu")
        collector.save_data()
        collector.close()
    except Exception as e:
        print(f"❌ Beklenmeyen hata: {e}")
        collector.save_data()
        collector.close()

if __name__ == "__main__":
    main()
