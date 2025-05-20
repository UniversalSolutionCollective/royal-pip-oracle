# oracle_main.py — Royal Oracle: Eternal Fire Edition 🔥

import asyncio
import socket
import time
from data_fetcher import fetch_twelvedata, fetch_binance
from signal_logic import generate_signal
from oracle_voice_utils import send_voice, send_telegram, log_signal
import pandas as pd

PAIRS = ['EUR/USD']
CRYPTO = ['BTCUSDT']
INTERVAL = '5min'

def is_connected():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

def mock_data(force_buy=True):
    prices = [1.1000] * 30
    df = pd.DataFrame({
        "open": prices,
        "high": [p + 0.001 for p in prices],
        "low": [p - 0.001 for p in prices],
        "close": prices
    })
    df.loc[df.index[-1], "close"] = 1.1050 if force_buy else 1.0950
    return df

def generate_forced_signal(pair, buy=True):
    side = "BUY" if buy else "SELL"
    msg = f"💥 FORCED {side} SIGNAL {pair} — [Fallback Mock Trigger]"
    return msg

async def process_pair(pair, is_crypto=False):
    df = None
    if is_connected():
        if is_crypto:
            df = fetch_binance(pair)
        else:
            df = fetch_twelvedata(pair, interval=INTERVAL)

    if df is None or df.empty:
        print(f"[{pair}] ⚠️ No real data — using mock fallback.")
        df = mock_data(force_buy=True)  # force a BUY condition

    signal = generate_signal(pair, df)

    if not signal:
        signal = generate_forced_signal(pair, buy=True)

    print(signal)
    await send_telegram(signal)
    await send_voice(signal, pair)
    log_signal(pair, signal)

async def main_loop():
    print("🟢 Royal Pip Oracle (FIRE MODE) is running...\n")
    while True:
        tasks = []
        for pair in PAIRS:
            tasks.append(process_pair(pair))
        for crypto in CRYPTO:
            tasks.append(process_pair(crypto, is_crypto=True))
        await asyncio.gather(*tasks)
        await asyncio.sleep(60)

if __name__ == "__main__":
    try:
        asyncio.run(main_loop())
    except KeyboardInterrupt:
        print("👑 Royal Oracle shut down.")
