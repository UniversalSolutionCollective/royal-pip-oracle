# data_fetcher.py — Royal Module 1: Live Market Data Engine

import requests
import pandas as pd

# === TwelveData API Key (already configured)
TWELVE_DATA_KEY = '333c20fe76504a32b594c03c1126d731'

def fetch_twelvedata(pair, interval='5min'):
    symbol = pair.replace("/", "")
    url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval={interval}&apikey={TWELVE_DATA_KEY}&outputsize=50"
    try:
        response = requests.get(url)
        values = response.json().get("values", [])
        if not values:
            print(f"[{pair}] ⚠️ TwelveData returned no data.")
            return pd.DataFrame()
        df = pd.DataFrame(values)
        df = df.rename(columns={"datetime": "time"}).set_index("time").astype(float)
        return df.sort_index()
    except Exception as e:
        print(f"[{pair}] ❌ TwelveData error:", e)
        return pd.DataFrame()

def fetch_binance(symbol='BTCUSDT', interval='5m'):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit=50"
    try:
        response = requests.get(url)
        klines = response.json()
        df = pd.DataFrame(klines, columns=[
            "time", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "num_trades",
            "taker_buy_base", "taker_buy_quote", "ignore"
        ])
        df = df[["open", "high", "low", "close"]].astype(float)
        return df
    except Exception as e:
        print(f"[{symbol}] ❌ Binance error:", e)
        return pd.DataFrame()
