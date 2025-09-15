import pandas as pd
import numpy as np
from transformers import pipeline
from datetime import datetime

class FundamentalAgent:
    def __init__(self):
        self.sentiment_analyzer = pipeline("sentiment-analysis")
        self.news_data = None
        
    def load_news_data(self, news_path):
        """تحميل بيانات الأخبار"""
        self.news_data = pd.read_csv(news_path)
        self.news_data['date'] = pd.to_datetime(self.news_data['published'])
        return self.news_data
    
    def analyze_sentiment_trend(self, days=7):
        """تحليل اتجاه المشاعر خلال فترة محددة"""
        recent_news = self.news_data[self.news_data['date'] >= (datetime.now() - timedelta(days=days))]
        
        if len(recent_news) == 0:
            return {"sentiment": "NEUTRAL", "confidence": 0.5, "sample_size": 0}
        
        positive_count = 0
        total_count = len(recent_news)
        
        for _, news in recent_news.iterrows():
            text = f"{news['title']} {news['summary']}"
            result = self.sentiment_analyzer(text[:512])
            if result[0]['label'] == 'POSITIVE':
                positive_count += 1
        
        sentiment_ratio = positive_count / total_count
        
        if sentiment_ratio > 0.6:
            return {"sentiment": "BULLISH", "confidence": sentiment_ratio, "sample_size": total_count}
        elif sentiment_ratio < 0.4:
            return {"sentiment": "BEARISH", "confidence": 1 - sentiment_ratio, "sample_size": total_count}
        else:
            return {"sentiment": "NEUTRAL", "confidence": 0.5, "sample_size": total_count}
    
    def generate_fundamental_signals(self):
        """توليد إشارات أساسية"""
        sentiment_analysis = self.analyze_sentiment_trend()
        
        return {
            'fundamental_sentiment': sentiment_analysis['sentiment'],
            'sentiment_confidence': sentiment_analysis['confidence'],
            'news_sample_size': sentiment_analysis['sample_size'],
            'recommendation': self._generate_recommendation(sentiment_analysis)
        }
    
    def _generate_recommendation(self, sentiment_data):
        """توليد توصية أساسية"""
        if sentiment_data['sentiment'] == 'BULLISH' and sentiment_data['confidence'] > 0.7:
            return "STRONG_BUY"
        elif sentiment_data['sentiment'] == 'BEARISH' and sentiment_data['confidence'] > 0.7:
            return "STRONG_SELL"
        else:
            return "HOLD"

# ✅ اختبار الوكيل
if __name__ == "__main__":
    # Initialize agent
    fundamental_agent = FundamentalAgent()
    
    # Load news data
    news_path = "../../data/raw/news/gold_news_with_sentiment.csv"
    fundamental_agent.load_news_data(news_path)
    
    # Generate signals
    signals = fundamental_agent.generate_fundamental_signals()
    
    print("🎯 إشارات الوكيل الأساسي:")
    for key, value in signals.items():
        print(f"{key}: {value}")
