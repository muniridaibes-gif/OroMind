import requests
import pandas as pd
import os
from datetime import datetime

# مفتاح API الخاص بك من Twelve Data
API_KEY = "AW6UTPFK0LWY06F4"
SYMBOL = "XAU/USD"
INTERVAL = "1day"
OUTPUT_SIZE = 1000  # عدد الأيام المطلوبة

def collect_gold_data():
    """
    دالة لجمع بيانات الذهب من Twelve Data API
    """
    try:
        # بناء رابط API
        url = f"https://api.twelvedata.com/time_series?symbol={SYMBOL}&interval={INTERVAL}&outputsize={OUTPUT_SIZE}&apikey={API_KEY}"
        
        # إرسال request إلى API
        response = requests.get(url)
        data = response.json()
        
        # التحقق من وجود البيانات
        if "values" not in data:
            print("❌ خطأ في response API:", data.get("message", "Unknown error"))
            return False
        
        # تحويل البيانات إلى DataFrame
        df = pd.DataFrame(data["values"])
        
        # ترتيب البيانات من الأقدم إلى الأحدث
        df = df.iloc[::-1].reset_index(drop=True)
        
        # إنشاء مجلد data إذا لم يكن موجودًا
        os.makedirs("../data", exist_ok=True)
        
        # حفظ البيانات في ملف CSV
        file_path = "../data/gold_data.csv"
        df.to_csv(file_path, index=False)
        
        print(f"✅ تم جمع وحفظ {len(df)} سجل بنجاح في {file_path}")
        print(f"📅 من {df['datetime'].iloc[0]} إلى {df['datetime'].iloc[-1]}")
        
        return True
        
    except Exception as e:
        print(f"❌ حدث خطأ: {str(e)}")
        return False

if __name__ == "__main__":
    collect_gold_data()
