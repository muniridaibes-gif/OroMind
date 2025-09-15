import pandas as pd
import pandas_datareader as pdr
from datetime import datetime

class EconomicDataCollector:
    def __init__(self):
        self.fred_codes = {
            'inflation': 'CPIAUCSL',      # التضخم
            'interest_rates': 'FEDFUNDS', # أسعار الفائدة
            'gdp': 'GDP',                 # الناتج المحلي
            'unemployment': 'UNRATE',     # البطالة
            'dollar_index': 'DTWEXB',     # مؤشر الدولار
        }
    
    def fetch_fred_data(self, start_date='2000-01-01'):
        """جمع البيانات من FRED"""
        economic_data = {}
        
        for name, code in self.fred_codes.items():
            try:
                print(f"📊 جلب بيانات {name}...")
                data = pdr.get_data_fred(code, start=start_date)
                economic_data[name] = data
                print(f"✅ تم جمع بيانات {name}")
            except Exception as e:
                print(f"❌ خطأ في جمع {name}: {str(e)}")
        
        return economic_data

    def save_economic_data(self, economic_data):
        """حفظ البيانات الاقتصادية"""
        os.makedirs('../../data/raw/economic', exist_ok=True)
        
        for name, data in economic_data.items():
            filename = f"../../data/raw/economic/{name}_data.csv"
            data.to_csv(filename)
            print(f"💾 تم حفظ {name} في {filename}")
