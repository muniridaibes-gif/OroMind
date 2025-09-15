import pandas as pd
from src.agents.technical_agent import TechnicalAgent
from src.agents.fundamental_agent import FundamentalAgent

class OroMindSystem:
    def __init__(self, gold_data_path, news_data_path):
        self.gold_data = pd.read_csv(gold_data_path)
        self.news_data_path = news_data_path
        self.technical_agent = TechnicalAgent(self.gold_data)
        self.fundamental_agent = FundamentalAgent()
        
    def run_analysis(self):
        """تشغيل التحليل المتكامل"""
        # تحليل فني
        technical_signals = self.technical_agent.generate_signals()
        
        # تحليل أساسي
        self.fundamental_agent.load_news_data(self.news_data_path)
        fundamental_signals = self.fundamental_agent.generate_fundamental_signals()
        
        # دمج النتائج
        final_decision = self._make_final_decision(technical_signals, fundamental_signals)
        
        return {
            'technical_analysis': technical_signals,
            'fundamental_analysis': fundamental_signals,
            'final_decision': final_decision,
            'timestamp': pd.Timestamp.now()
        }
    
    def _make_final_decision(self, technical, fundamental):
        """اتخاذ القرار النهائي"""
        # منطق دمج الإشارات
        if technical['recommendation'] == 'BUY' and fundamental['recommendation'] == 'STRONG_BUY':
            return 'STRONG_BUY'
        elif technical['recommendation'] == 'SELL' and fundamental['recommendation'] == 'STRONG_SELL':
            return 'STRONG_SELL'
        else:
            return 'HOLD'

# ✅ اختبار النظام
if __name__ == "__main__":
    system = OroMindSystem(
        gold_data_path="../../data/raw/gold/gold_historical_7148_days.csv",
        news_data_path="../../data/raw/news/gold_news_with_sentiment.csv"
    )
    
    result = system.run_analysis()
    
    print("🧠 نتائج نظام OroMind المتكامل:")
    print(f"📊 التوصية النهائية: {result['final_decision']}")
    print(f"⏰ وقت التحليل: {result['timestamp']}")
