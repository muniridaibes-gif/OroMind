import pandas as pd
from transformers import pipeline
import logging

class FundamentalAgent:
    def __init__(self):
        self.sentiment_analyzer = pipeline("sentiment-analysis")
        self.setup_logging()
    
    def setup_logging(self):
        """إعداد نظام التسجيل"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    def analyze_news_sentiment(self, input_file, output_file):
        """
        تحليل مشاعر الأخبار وحفظ النتائج
        """
        try:
            # تحميل بيانات الأخبار
            logging.info(f"📖 جاري تحميل الأخبار من: {input_file}")
            news_df = pd.read_csv(input_file)
            
            sentiments = []
            confidence_scores = []
            
            logging.info(f"🔍 بدء تحليل مشاعر {len(news_df)} خبر...")
            
            for index, row in news_df.iterrows():
                try:
                    # دمج العنوان والمحتوى للتحليل
                    text = f"{row['title']}. {row.get('summary', '')}"[:512]
                    result = self.sentiment_analyzer(text)
                    
                    sentiments.append(result[0]['label'])
                    confidence_scores.append(result[0]['score'])
                    
                except Exception as e:
                    sentiments.append("NEUTRAL")
                    confidence_scores.append(0.5)
                    logging.warning(f"⚠️ خطأ في تحليل الخبر {index}: {str(e)}")
            
            # إضافة النتائج إلى DataFrame
            news_df['sentiment'] = sentiments
            news_df['sentiment_confidence'] = confidence_scores
            
            # حفظ النتائج
            news_df.to_csv(output_file, index=False)
            logging.info(f"💾 تم حفظ النتائج في: {output_file}")
            
            return news_df
            
        except Exception as e:
            logging.error(f"❌ خطأ في تحليل المشاعر: {str(e)}")
            return None

# التشغيل المباشر إذا تم تنفيذ الملف
if __name__ == "__main__":
    # Initialize the agent
    agent = FundamentalAgent()
    
    # Analyze sentiment and create the missing file
    result = agent.analyze_news_sentiment(
        "../data/raw/news/gold_related_news.csv",
        "../data/raw/news/gold_news_with_sentiment.csv"
    )
    
    if result is not None:
        print("✅ تم إنشاء gold_news_with_sentiment.csv بنجاح!")
        print(f"📊 عدد الأخبار المحللة: {len(result)}")
    else:
        print("❌ فشل في إنشاء الملف")
