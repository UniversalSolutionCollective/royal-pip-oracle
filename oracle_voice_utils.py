# oracle_voice_utils.py — Royal Module 3: Voice & Messenger Core

import os
import csv
import time
import edge_tts
from telegram import Bot

# === Credentials
TELEGRAM_TOKEN = '7692005972:AAFT1-OXwDRdyTiFwqrBz4XMfKc2srQcoKc'
CHAT_ID = '1284230764'
LOG_FILE = 'oracle_signals.csv'

# === Initialize Telegram Bot
bot = Bot(token=TELEGRAM_TOKEN)

# === Voice alert system using Edge TTS
async def send_voice(message, pair):
    try:
        filename = f"oracle_voice_{pair.replace('/', '_')}.mp3"
        communicate = edge_tts.Communicate(text=message, voice="en-GB-RyanNeural")
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                with open(filename, "ab") as f:
                    f.write(chunk["data"])
        os.system(f'start {filename}')
    except Exception as e:
        print(f"[{pair}] Voice error:", e)

# === Telegram alert sender
async def send_telegram(message):
    try:
        await bot.send_message(chat_id=CHAT_ID, text=message)
    except Exception as e:
        print("Telegram error:", e)

# === CSV logging
def log_signal(pair, message):
    os.makedirs("logs", exist_ok=True)
    with open(f"logs/{LOG_FILE}", mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), pair, message])
