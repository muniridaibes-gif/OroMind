import pandas as pd
import requests
from datetime import datetime
import logging

class DailyUpdater:
    def __init__(self, api_key):
        self.api_key = api_key
        self.setup_logging()
    
    def setup_logging(self):
        """إعداد نظام التسجيل"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    def initialize_daily_file(self):
        """
        إنشاء ملف التحديثات اليومية الأولي
        """
        try:
            # إنشاء DataFrame بهيكل واضح
            columns = [
                'datetime', 'open', 'high', 'low', 'close', 'volume',
                'update_type', 'data_source', 'timestamp'
            ]
            
            daily_df = pd.DataFrame(columns=columns)
            
            # حفظ الملف
            file_path = "../data/raw/gold/gold_daily_updates.csv"
            daily_df.to_csv(file_path, index=False)
            
            logging.info(f"✅ تم إنشاء {file_path} بنجاح")
            return True
            
        except Exception as e:
            logging.error(f"❌ خطأ في إنشاء الملف: {str(e)}")
            return False
    
    def add_daily_update(self, new_data):
        """
        إضافة تحديث يومي جديد للملف
        """
        try:
            # تحميل الملف الحالي
            daily_df = pd.read_csv("../data/raw/gold/gold_daily_updates.csv")
            
            # إضافة البيانات الجديدة
            updated_df = pd.concat([daily_df, new_data], ignore_index=True)
            
            # حفظ الملف المحدث
            updated_df.to_csv("../data/raw/gold/gold_daily_updates.csv", index=False)
            
            logging.info(f"📈 تم إضافة {len(new_data)} تحديث جديد")
            return True
            
        except Exception as e:
            logging.error(f"❌ خطأ في إضافة التحديث: {str(e)}")
            return False

# التشغيل المباشر
if __name__ == "__main__":
    # Initialize updater
    updater = DailyUpdater("9fe19365755a4339ae1e7a1392fcd8e6")
    
    # Create the initial file
    success = updater.initialize_daily_file()
    
    if success:
        print("✅ تم إنشاء gold_daily_updates.csv بنجاح!")
        print("📁 الملف جاهز للتحديثات اليومية المستقبلية")
    else:
        print("❌ فشل في إنشاء الملف")
