import schedule
import time
import pandas as pd
from datetime import datetime, timedelta
import requests
import logging
from google.colab import files

class DailyUpdater:
    def __init__(self, api_key):
        self.api_key = api_key
        self.setup_logging()
        
    def setup_logging(self):
        """إعداد نظام التسجيل"""
        logging.basicConfig(
            filename='data_update.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    def update_gold_prices(self):
        """تحديث أسعار الذهب اليومية"""
        try:
            url = f"https://api.twelvedata.com/time_series?symbol=XAU/USD&interval=1day&outputsize=2&apikey={self.api_key}"
            response = requests.get(url)
            data = response.json()
            
            if "values" in data:
                new_data = pd.DataFrame(data["values"])
                new_data = new_data.iloc[::-1]
                
                # تحميل البيانات القديمة
                historical_data = pd.read_csv('../data/raw/gold/gold_historical_7148_days.csv')
                
                # دمج البيانات الجديدة
                updated_data = pd.concat([historical_data, new_data], ignore_index=True)
                updated_data = updated_data.drop_duplicates('datetime')
                
                # حفظ البيانات المحدثة
                updated_data.to_csv('../data/raw/gold/gold_historical_updated.csv', index=False)
                
                logging.info(f"✅ تم تحديث بيانات الذهب: {len(new_data)} يوم جديد")
                return True
                
        except Exception as e:
            logging.error(f"❌ خطأ في تحديث الذهب: {str(e)}")
            return False
    
    def update_news(self):
        """تحديث الأخبار اليومية"""
        try:
            # كود جمع الأخبار الذي لديك
            news_df = self.collect_daily_news()
            news_df.to_csv('../data/raw/news/daily_news.csv', mode='a', header=False)
            
            logging.info(f"✅ تم تحديث الأخبار: {len(news_df)} خبر جديد")
            return True
            
        except Exception as e:
            logging.error(f"❌ خطأ في تحديث الأخبار: {str(e)}")
            return False
    
    def run_daily_updates(self):
        """تشغيل التحديثات اليومية"""
        logging.info("🚀 بدء التحديثات اليومية")
        
        # جدولة المهام
        schedule.every().day.at("08:00").do(self.update_gold_prices)
        schedule.every().hour().do(self.update_news)
        
        while True:
            schedule.run_pending()
            time.sleep(60)

# ✅ التشغيل الفوري
if __name__ == "__main__":
    updater = DailyUpdater("9fe19365755a4339ae1e7a1392fcd8e6")
    
    # تحديث فوري للاختبار
    updater.update_gold_prices()
    updater.update_news()
    
    print("✅ تم التحديث اليومي بنجاح!")
