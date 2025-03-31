
import pandas as pd
import pandas_ta as ta
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime, timedelta
import os
import json

api_key = os.getenv("ALPACA_API_KEY")
secret_key = os.getenv("ALPACA_SECRET_KEY")

client = StockHistoricalDataClient(api_key, secret_key)

SP500 = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "BRK.B", "UNH", "V", "XOM", "JNJ", "JPM", "LLY", "PG", "AVGO", "MA", "HD", "CVX", "MRK"]  # Sample only

seen_flips = {}

def get_bars(symbol):
    end = datetime.utcnow()
    start = end - timedelta(days=100)
    request = StockBarsRequest(
        symbol_or_symbols=symbol,
        timeframe=TimeFrame.Day,
        start=start,
        end=end
    )
    bars = client.get_stock_bars(request).df
    if bars.empty or symbol not in bars.index.levels[0]:
        return None
    return bars.xs(symbol, level=0)

def calculate_supertrend(df):
    st = ta.supertrend(df['high'], df['low'], df['close'], length=10, multiplier=3.0)
    return df.join(st)

def check_recent_flips(df, symbol, days=5):
    for i in range(-days, -1):
        if i < -len(df):
            continue
        prev = df.iloc[i - 1]
        curr = df.iloc[i]
        flip_date = str(curr.name.date())
        if prev['SUPERT_10_3.0'] > prev['close'] and curr['SUPERT_10_3.0'] < curr['close']:
            if seen_flips.get(symbol) != flip_date:
                seen_flips[symbol] = flip_date
                return flip_date
    return None

def scan():
    for symbol in SP500:
        try:
            df = get_bars(symbol)
            if df is None or len(df) < 6:
                continue
            df = calculate_supertrend(df)
            check_recent_flips(df, symbol)
        except Exception as e:
            print(f"{symbol} error: {e}")

    with open("public_flips.json", "w") as f:
        json.dump(seen_flips, f, indent=2)

if __name__ == "__main__":
    scan()
