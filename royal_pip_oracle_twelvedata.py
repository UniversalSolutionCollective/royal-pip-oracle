# royal_pip_oracle_twelvedata.py 👑 FINAL FORM

import requests
import pandas as pd
import asyncio
import csv
import os
import time
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator
from telegram import Bot
import edge_tts

# === ROYAL CONFIGURATION ===
TELEGRAM_TOKEN = '7692005972:AAFT1-OXwDRdyTiFwqrBz4XMfKc2srQcoKc'
CHAT_ID = '1284230764'
TWELVE_DATA_KEY = '333c20fe76504a32b594c03c1126d731'
PAIRS = ['EUR/USD', 'GBP/USD', 'XAU/USD', 'BTC/USD']
INTERVAL = '5min'
LOG_FILE = 'oracle_signals.csv'

bot = Bot(token=TELEGRAM_TOKEN)

async def send_voice(message):
    try:
        communicate = edge_tts.Communicate(text=message, voice="en-GB-RyanNeural")
        await communicate.run()
    except Exception as e:
        print("Voice error:", e)

async def send_telegram(message):
    try:
        await bot.send_message(chat_id=CHAT_ID, text=message)
    except Exception as e:
        print("Telegram error:", e)

def log_signal(pair, message):
    os.makedirs("logs", exist_ok=True)
    with open(f"logs/{LOG_FILE}", mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), pair, message])

def fetch_data(pair):
    symbol = pair.replace("/", "")
    url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval={INTERVAL}&apikey={TWELVE_DATA_KEY}&outputsize=50"
    try:
        r = requests.get(url)
        data = r.json().get("values", [])
        if not data:
            print(f"[{pair}] ⚠️ No data received.")
            return pd.DataFrame()
        df = pd.DataFrame(data)
        df = df.rename(columns={"datetime": "time"}).set_index("time").astype(float)
        return df.sort_index()
    except Exception as e:
        print(f"[{pair}] ❌ Data fetch error:", e)
        return pd.DataFrame()

def generate_signal(pair, df):
    if df.empty or len(df) < 20:
        return None
    df['rsi'] = RSIIndicator(df['close'], window=14).rsi()
    df['ema'] = EMAIndicator(df['close'], window=10).ema_indicator()
    last = df.iloc[-1]
    if last['rsi'] < 30 and last['close'] > last['ema']:
        return f"BUY 🔥 {pair} — RSI < 30 & Price > EMA"
    elif last['rsi'] > 70 and last['close'] < last['ema']:
        return f"SELL 🚨 {pair} — RSI > 70 & Price < EMA"
    return None

async def main_loop():
    print("🟢 Royal Pip Oracle Supreme (TwelveData) is LIVE...\n")
    while True:
        for pair in PAIRS:
            df = fetch_data(pair)
            signal = generate_signal(pair, df)
            if signal:
                print(signal)
                await send_telegram(signal)
                await send_voice(signal)
                log_signal(pair, signal)
            else:
                print(f"— {pair}: No signal this round.")
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main_loop())
