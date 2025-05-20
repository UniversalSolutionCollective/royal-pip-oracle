# signal_logic.py — Royal Module 2: RSI + EMA Signal Engine

from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator
import pandas as pd

def generate_signal(pair, df):
    if df.empty or len(df) < 20:
        return None
    
    # Calculate indicators
    df['rsi'] = RSIIndicator(df['close'], window=14).rsi()
    df['ema'] = EMAIndicator(df['close'], window=10).ema_indicator()
    
    # Get last candle data
    last = df.iloc[-1]

    # Define signal logic
    if last['rsi'] < 30 and last['close'] > last['ema']:
        return f"🔥 BUY SIGNAL {pair} — RSI: {last['rsi']:.2f}, Price above EMA"
    elif last['rsi'] > 70 and last['close'] < last['ema']:
        return f"🚨 SELL SIGNAL {pair} — RSI: {last['rsi']:.2f}, Price below EMA"
    
    return None
