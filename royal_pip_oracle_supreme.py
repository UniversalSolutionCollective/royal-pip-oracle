# royal_pip_oracle_supreme.py 👑 FINAL FORM

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

# === NO MANUAL SETUP — DIVINE CONFIG ===
TELEGRAM_TOKEN = '7692005972:AAFT1-OXwDRdyTiFwqrBz4XMfKc2srQcoKc'
CHAT_ID = '1284230764'
ALPHA_VANTAGE_KEY = 'P7GJPYL7KFLBCQEP'

# Monitor these pairs — feel free to add more
PAIRS = ['EURUSD']
INTERVAL = '15min'
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
    if pair == 'BTCUSD':
        url = f"https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_INTRADAY&symbol=BTC&market=USD&apikey={ALPHA_VANTAGE_KEY}"
        r = requests.get(url)
        data = r.json().get("Time Series (Digital Currency Intraday)", {})
    else:
        base, quote = pair[:3], pair[3:]
        url = f"https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol={base}&to_symbol={quote}&interval={INTERVAL}&apikey={ALPHA_VANTAGE_KEY}"
        r = requests.get(url)
        data = r.json().get(f"Time Series FX ({INTERVAL})", {})

    if not data:
        print(f"[{pair}] ⚠️ No data received.")
        return pd.DataFrame()

    df = pd.DataFrame(data).T.astype(float)
    df.columns = ['open', 'high', 'low', 'close']
    return df

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
    print("🟢 Royal Pip Oracle Supreme is LIVE...\n")
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
