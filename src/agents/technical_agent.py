import pandas as pd
import numpy as np
import talib

class TechnicalAgent:
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path)
        self.prepare_data()
        self.calculate_indicators()
    
    def prepare_data(self):
        """تحضير البيانات الأساسية"""
        self.data['datetime'] = pd.to_datetime(self.data['datetime'])
        self.data = self.data.sort_values('datetime')
        print(f"✅ تم تحميل {len(self.data)} يوم من البيانات")
    
    def calculate_indicators(self):
        """حساب المؤشرات الفنية"""
        close = self.data['close'].values
        
        # المتوسطات المتحركة
        self.data['SMA_20'] = talib.SMA(close, timeperiod=20)
        self.data['SMA_50'] = talib.SMA(close, timeperiod=50)
        self.data['EMA_14'] = talib.EMA(close, timeperiod=14)
        
        # مؤشرات الزخم
        self.data['RSI'] = talib.RSI(close, timeperiod=14)
        self.data['MACD'], self.data['MACD_signal'], _ = talib.MACD(close)
        
        print("✅ تم حساب جميع المؤشرات الفنية")
    
    def generate_signals(self):
        """توليد إشارات تداول"""
        latest = self.data.iloc[-1]
        
        signals = {
            'trend_bullish': latest['SMA_20'] > latest['SMA_50'],
            'rsi_level': latest['RSI'],
            'macd_bullish': latest['MACD'] > latest['MACD_signal'],
            'recommendation': self._generate_recommendation(latest)
        }
        
        return signals
    
    def _generate_recommendation(self, data):
        """توليد توصية"""
        if data['RSI'] < 30 and data['SMA_20'] > data['SMA_50']:
            return "STRONG_BUY"
        elif data['RSI'] > 70 and data['SMA_20'] < data['SMA_50']:
            return "STRONG_SELL"
        else:
            return "HOLD"

if __name__ == "__main__":
    agent = TechnicalAgent("../data/raw/gold/gold_historical_7148_days.csv")
    signals = agent.generate_signals()
    print("🎯 إشارات الوكيل الفني:", signals)
