import requests
import pandas as pd
import asyncio
import time
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator
from telegram import Bot

TELEGRAM_TOKEN = 'your_bot_token'
CHAT_ID = 'your_chat_id'
ALPHA_VANTAGE_KEY = 'your_av_key'
PAIR = 'EURUSD'
INTERVAL = '5min'

bot = Bot(token=TELEGRAM_TOKEN)

async def send_telegram(message):
    await bot.send_message(chat_id=CHAT_ID, text=message)

def fetch_data():
    url = f"https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol=EUR&to_symbol=USD&interval={INTERVAL}&apikey={ALPHA_VANTAGE_KEY}"
    r = requests.get(url)
    data = r.json().get(f"Time Series FX ({INTERVAL})", {})
    if not data:
        return pd.DataFrame()
    df = pd.DataFrame(data).T.astype(float)
    df.columns = ['open', 'high', 'low', 'close']
    return df

def generate_signal(df):
    if df.empty or len(df) < 20:
        return None
    df['rsi'] = RSIIndicator(df['close'], window=14).rsi()
    df['ema'] = EMAIndicator(df['close'], window=10).ema_indicator()
    last = df.iloc[-1]
    if last['rsi'] < 30 and last['close'] > last['ema']:
        return "BUY 🔥 EURUSD — RSI < 30 and above EMA"
    elif last['rsi'] > 70 and last['close'] < last['ema']:
        return "SELL 🚨 EURUSD — RSI > 70 and below EMA"
    return None

while True:
    df = fetch_data()
    signal = generate_signal(df)
    if signal:
        print(signal)
        asyncio.run(send_telegram(signal))
    else:
        print("No signal this round.")
    time.sleep(60)
