import requests
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta
import os

class GoldDataCollector:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.twelvedata.com/time_series"
        
    def fetch_historical_data(self, symbol="XAU/USD", interval="1day", output_size=7500):
        """جمع البيانات التاريخية للذهب"""
        params = {
            'symbol': symbol,
            'interval': interval,
            'outputsize': output_size,
            'apikey': self.api_key
        }
        
        try:
            print("🔍 بدء جمع بيانات الذهب التاريخية...")
            response = requests.get(self.base_url, params=params)
            data = response.json()
            
            if "values" in data:
                df = pd.DataFrame(data["values"])
                df = df.iloc[::-1].reset_index(drop=True)
                
                # تحويل أنواع البيانات
                numeric_columns = ['open', 'high', 'low', 'close', 'volume']
                for col in numeric_columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                
                df['datetime'] = pd.to_datetime(df['datetime'])
                
                print(f"✅ تم جمع {len(df)} يوم من البيانات")
                print(f"📅 الفترة من {df['datetime'].iloc[0]} إلى {df['datetime'].iloc[-1]}")
                
                return df
            else:
                print("❌ خطأ في جمع البيانات:", data.get('message', 'Unknown error'))
                return None
                
        except Exception as e:
            print(f"❌ حدث خطأ: {str(e)}")
            return None
    
    def save_data(self, df, filename="gold_historical_data.csv"):
        """حفظ البيانات في ملف CSV"""
        if df is not None:
            os.makedirs('../../data/raw/gold', exist_ok=True)
            filepath = f'../../data/raw/gold/{filename}'
            df.to_csv(filepath, index=False)
            print(f"💾 تم حفظ البيانات في: {filepath}")
            return filepath
        return None

# الكود الرئيسي
if __name__ == "__main__":
    # مفتاح API الخاص بك
    API_KEY = "9fe19365755a4339ae1e7a1392fcd8e6"
    
    # إنشاء الكوليكتور
    collector = GoldDataCollector(API_KEY)
    
    # جمع البيانات
    gold_data = collector.fetch_historical_data(output_size=7500)
    
    # حفظ البيانات
    if gold_data is not None:
        collector.save_data(gold_data)
        print("🎉 اكتمل جمع البيانات بنجاح!")
    else:
        print("❌ فشل في جمع البيانات")
