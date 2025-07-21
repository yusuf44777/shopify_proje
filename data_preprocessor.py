import json
import pandas as pd
import os
from datetime import datetime
import re
from typing import List, Dict, Any

class DataPreprocessor:
    def __init__(self, data_dir="shopify_training_data"):
        self.data_dir = data_dir
        self.processed_data = []
        
    def load_raw_data(self):
        """Ham verileri yükle"""
        all_data = []
        
        # JSON dosyalarını yükle
        for filename in os.listdir(self.data_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.data_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            all_data.extend(data)
                        else:
                            all_data.append(data)
                    print(f"✅ Yüklendi: {filepath} ({len(data) if isinstance(data, list) else 1} kayıt)")
                except Exception as e:
                    print(f"❌ Yükleme hatası {filepath}: {e}")
        
        print(f"📊 Toplam ham veri: {len(all_data)} kayıt")
        return all_data
    
    def clean_text(self, text):
        """Metni temizle ve normalize et"""
        if not text or not isinstance(text, str):
            return ""
        
        # HTML etiketlerini kaldır
        text = re.sub(r'<[^>]+>', ' ', text)
        
        # Fazla boşlukları temizle
        text = re.sub(r'\s+', ' ', text)
        
        # Özel karakterleri temizle
        text = re.sub(r'[^\w\s\.,!?;:()-]', ' ', text)
        
        # Baştan ve sondan boşlukları kaldır
        text = text.strip()
        
        return text
    
    def extract_features(self, product_data):
        """Ürün verisinden özellikler çıkar"""
        features = {
            'title': self.clean_text(product_data.get('title', '')),
            'description': self.clean_text(product_data.get('description', '')),
            'category': self.clean_text(product_data.get('category', '')),
            'price': product_data.get('price', ''),
            'features_list': product_data.get('features', [])
        }
        
        # Fiyat işleme
        if features['price']:
            # Fiyattan sadece sayıları çıkar
            price_match = re.search(r'[\d,]+\.?\d*', str(features['price']))
            if price_match:
                features['price_numeric'] = float(price_match.group().replace(',', ''))
            else:
                features['price_numeric'] = 0
        else:
            features['price_numeric'] = 0
        
        # Açıklama uzunluğu
        features['description_length'] = len(features['description'])
        
        # Başlık uzunluğu
        features['title_length'] = len(features['title'])
        
        # Anahtar kelime sayısı
        features['title_word_count'] = len(features['title'].split())
        features['description_word_count'] = len(features['description'].split())
        
        return features
    
    def create_training_prompts(self, product_data):
        """Eğitim için prompt-response çiftleri oluştur"""
        features = self.extract_features(product_data)
        
        training_examples = []
        
        # 1. Başlık oluşturma görevi
        if features['title'] and features['category']:
            prompt = f"Create a compelling Shopify product title for a {features['category']} product."
            response = features['title']
            training_examples.append({
                'instruction': prompt,
                'input': '',
                'output': response,
                'task_type': 'title_generation'
            })
        
        # 2. Açıklama oluşturma görevi
        if features['description'] and features['title']:
            prompt = f"Write a detailed Shopify product description for: {features['title']}"
            response = features['description']
            training_examples.append({
                'instruction': prompt,
                'input': '',
                'output': response,
                'task_type': 'description_generation'
            })
        
        # 3. Anahtar kelimeye dayalı açıklama
        if features['description'] and features['category']:
            prompt = f"Generate a Shopify product description for a {features['category']} product."
            response = features['description']
            training_examples.append({
                'instruction': prompt,
                'input': '',
                'output': response,
                'task_type': 'category_description'
            })
        
        # 4. Özellik listesine dayalı açıklama
        if features['description'] and features['features_list']:
            features_text = ', '.join(features['features_list'][:5])  # İlk 5 özellik
            prompt = f"Create a product description based on these features: {features_text}"
            response = features['description']
            training_examples.append({
                'instruction': prompt,
                'input': '',
                'output': response,
                'task_type': 'feature_description'
            })
        
        return training_examples
    
    def process_data(self):
        """Verileri işle ve eğitim formatına dönüştür"""
        print("🔄 Veri işleme başlıyor...")
        
        raw_data = self.load_raw_data()
        all_training_examples = []
        
        for i, product in enumerate(raw_data):
            try:
                training_examples = self.create_training_prompts(product)
                all_training_examples.extend(training_examples)
                
                if (i + 1) % 100 == 0:
                    print(f"📋 İşlenen ürün sayısı: {i + 1}")
                    
            except Exception as e:
                print(f"❌ Ürün işleme hatası {i}: {e}")
        
        print(f"✅ Toplam eğitim örneği: {len(all_training_examples)}")
        return all_training_examples
    
    def save_training_data(self, training_data, format_type="alpaca"):
        """Eğitim verisini kaydet"""
        output_dir = "model_training_data"
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        
        if format_type == "alpaca":
            # Alpaca formatında kaydet
            filename = f"shopify_alpaca_training_{timestamp}.json"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(training_data, f, ensure_ascii=False, indent=2)
        
        elif format_type == "jsonl":
            # JSONL formatında kaydet (her satırda bir JSON)
            filename = f"shopify_training_{timestamp}.jsonl"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                for example in training_data:
                    f.write(json.dumps(example, ensure_ascii=False) + '\n')
        
        elif format_type == "csv":
            # CSV formatında kaydet
            filename = f"shopify_training_{timestamp}.csv"
            filepath = os.path.join(output_dir, filename)
            
            df = pd.DataFrame(training_data)
            df.to_csv(filepath, index=False, encoding='utf-8')
        
        print(f"💾 Eğitim verisi kaydedildi: {filepath}")
        return filepath
    
    def create_validation_split(self, training_data, validation_ratio=0.1):
        """Eğitim ve doğrulama setlerini ayır"""
        import random
        
        # Veriyi karıştır
        random.shuffle(training_data)
        
        # Bölme noktasını hesapla
        split_index = int(len(training_data) * (1 - validation_ratio))
        
        train_data = training_data[:split_index]
        val_data = training_data[split_index:]
        
        print(f"📊 Eğitim seti: {len(train_data)} örnek")
        print(f"📊 Doğrulama seti: {len(val_data)} örnek")
        
        return train_data, val_data
    
    def generate_statistics(self, training_data):
        """Veri istatistikleri oluştur"""
        stats = {
            'total_examples': len(training_data),
            'task_types': {},
            'avg_input_length': 0,
            'avg_output_length': 0,
            'output_length_distribution': {}
        }
        
        total_input_length = 0
        total_output_length = 0
        output_lengths = []
        
        for example in training_data:
            # Görev türü istatistikleri
            task_type = example.get('task_type', 'unknown')
            stats['task_types'][task_type] = stats['task_types'].get(task_type, 0) + 1
            
            # Uzunluk istatistikleri
            input_length = len(example.get('input', '') + example.get('instruction', ''))
            output_length = len(example.get('output', ''))
            
            total_input_length += input_length
            total_output_length += output_length
            output_lengths.append(output_length)
        
        stats['avg_input_length'] = total_input_length / len(training_data) if training_data else 0
        stats['avg_output_length'] = total_output_length / len(training_data) if training_data else 0
        
        # Çıktı uzunluk dağılımı
        if output_lengths:
            stats['min_output_length'] = min(output_lengths)
            stats['max_output_length'] = max(output_lengths)
            stats['median_output_length'] = sorted(output_lengths)[len(output_lengths)//2]
        
        return stats

def main():
    """Ana fonksiyon"""
    print("🚀 Shopify veri ön işleme başlıyor...")
    
    preprocessor = DataPreprocessor()
    
    try:
        # Veriyi işle
        training_data = preprocessor.process_data()
        
        if not training_data:
            print("❌ İşlenecek veri bulunamadı!")
            return
        
        # Eğitim ve doğrulama setlerini ayır
        train_data, val_data = preprocessor.create_validation_split(training_data)
        
        # Farklı formatlarda kaydet
        print("💾 Eğitim verisi kaydediliyor...")
        preprocessor.save_training_data(train_data, "alpaca")
        preprocessor.save_training_data(train_data, "jsonl")
        
        # Doğrulama setini kaydet
        preprocessor.save_training_data(val_data, "alpaca")
        
        # İstatistikleri oluştur ve kaydet
        stats = preprocessor.generate_statistics(training_data)
        
        stats_file = f"model_training_data/data_statistics_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
        
        print("📊 Veri İstatistikleri:")
        print(f"  - Toplam örnek: {stats['total_examples']}")
        print(f"  - Ortalama giriş uzunluğu: {stats['avg_input_length']:.1f}")
        print(f"  - Ortalama çıkış uzunluğu: {stats['avg_output_length']:.1f}")
        print(f"  - Görev türleri: {stats['task_types']}")
        
        print("✅ Veri ön işleme tamamlandı!")
        
    except Exception as e:
        print(f"❌ Hata oluştu: {e}")

if __name__ == "__main__":
    main()
