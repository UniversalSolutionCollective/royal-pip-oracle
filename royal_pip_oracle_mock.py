import pandas as pd
import asyncio
import csv
import os
import time
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator
from telegram import Bot
import edge_tts

TELEGRAM_TOKEN = '7692005972:AAFT1-OXwDRdyTiFwqrBz4XMfKc2srQcoKc'
CHAT_ID = '1284230764'
PAIRS = ['EUR/USD', 'GBP/USD', 'XAU/USD', 'BTC/USD']
LOG_FILE = 'oracle_signals_mock.csv'

bot = Bot(token=TELEGRAM_TOKEN)

async def send_voice(message, pair):
    try:
        filename = f"oracle_voice_{pair.replace('/', '_')}.mp3"
        communicate = edge_tts.Communicate(text=message, voice="en-GB-RyanNeural")
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                with open(filename, "ab") as f:
                    f.write(chunk["data"])
        os.system(f'start {filename}')  # Windows
    except Exception as e:
        print(f"Voice error for {pair}:", e)

async def send_telegram(message):
    try:
        await bot.send_message(chat_id=CHAT_ID, text=message)
    except Exception as e:
        print("Telegram error:", e)

def log_signal(pair, message):
    os.makedirs("logs", exist_ok=True)
    with open(f"logs/{LOG_FILE}", mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), pair, message])

def generate_mock_data():
    data = {
        "open": [1.1000]*30,
        "high": [1.1050]*30,
        "low": [1.0950]*30,
        "close": [1.1020]*30
    }
    df = pd.DataFrame(data)
    df.loc[df.index[-1], "close"] = 1.1045
    return df

def generate_signal(pair, df):
    if df.empty or len(df) < 20:
        return None
    df['rsi'] = RSIIndicator(df['close'], window=14).rsi()
    df['ema'] = EMAIndicator(df['close'], window=10).ema_indicator()
    last = df.iloc[-1]
    if last['rsi'] < 70:
        return f"🔥 TEST BUY SIGNAL {pair} — RSI: {last['rsi']:.2f}, Close > EMA"
    elif last['rsi'] > 30:
        return f"🚨 TEST SELL SIGNAL {pair} — RSI: {last['rsi']:.2f}, Close < EMA"
    return None

async def main_loop():
    print("🧪 Royal Pip Oracle (MOCK MODE) is running...\n")
    while True:
        for pair in PAIRS:
            df = generate_mock_data()
            signal = generate_signal(pair, df)
            if signal:
                print(signal)
                await send_telegram(signal)
                await send_voice(signal, pair)
                log_signal(pair, signal)
            else:
                print(f"— {pair}: No signal in mock.")
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main_loop())
