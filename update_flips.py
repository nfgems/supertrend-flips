import pandas as pd
import pandas_ta as ta
from alpaca.data.historical.stock import StockHistoricalDataClient 
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime, timedelta
import os
import json

api_key = os.getenv("ALPACA_API_KEY")
secret_key = os.getenv("ALPACA_SECRET_KEY")

client = StockHistoricalDataClient(api_key, secret_key)

SP500 = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "BRK.B", "UNH", "V",
    "XOM", "JNJ", "JPM", "LLY", "PG", "AVGO", "MA", "HD", "CVX", "MRK",
    "ABBV", "COST", "PEP", "KO", "BAC", "ADBE", "CRM", "WMT", "PFE", "NFLX",
    "TMO", "ACN", "ABT", "LIN", "ORCL", "DIS", "NKE", "CSCO", "MCD", "CMCSA",
    "DHR", "AMD", "INTC", "QCOM", "TXN", "NEE", "HON", "AMGN", "PM", "UPS",
    "UNP", "MS", "IBM", "BMY", "GS", "LOW", "RTX", "GE", "SPGI", "CAT",
    "ISRG", "AMT", "SBUX", "MDT", "INTU", "VRTX", "T", "BLK", "NOW", "CI",
    "CVS", "ADI", "DE", "ZTS", "SYK", "MDLZ", "AXP", "C", "ELV", "MO",
    "REGN", "GILD", "MU", "PLD", "BKNG", "LRCX", "PANW", "ADP", "TJX", "SCHW",
    "CL", "FISV", "MMC", "CB", "HCA", "LMT", "TGT", "APD", "DUK", "F",
    "WM", "PGR", "SO", "EOG", "ETN", "NSC", "SHW", "BDX", "EMR", "ITW",
    "FDX", "COF", "PSX", "HUM", "CME", "NOC", "EW", "MAR", "AON", "OXY",
    "ADSK", "MET", "ROST", "MNST", "STZ", "AIG", "KMB", "MCO", "AFL", "GIS",
    "SLB", "IDXX", "AJG", "VLO", "PRU", "ORLY", "KMI", "EXC", "PEG", "PSA",
    "DVN", "DLR", "CTSH", "HSY", "PCAR", "MSCI", "BKR", "TRV", "ALL", "HPQ",
    "HLT", "SRE", "SPG", "KHC", "ED", "YUM", "AME", "AZO", "MTD", "PXD",
    "TEL", "MCK", "CMG", "KR", "WELL", "IQV", "WMB", "AEP", "FAST", "TT",
    "DLTR", "EFX", "VRSK", "AMP", "CHD", "WST", "CDNS", "WTW", "CTVA", "ANET",
    "FTNT", "BIIB", "ECL", "VFC", "PAYX", "TSCO", "HES", "RSG", "WBD", "MLM",
    "OTIS", "KEYS", "PPL", "FANG", "CNC", "OKE", "AVB", "FLT", "NEM", "D",
    "HAL", "SBAC", "ODFL", "CMS", "ABC", "PH", "INVH", "IR", "TTWO", "VTR",
    "RMD", "CBRE", "XYL", "DPZ", "TSN", "EXR", "CARR", "BR", "CEG", "DRI",
    "GWW", "BALL", "LDOS", "DG", "IFF", "PPG", "MAS", "CFG", "HBAN", "ZBRA",
    "NUE", "LUV", "ALB", "LHX", "CTRA", "CLX", "DOV", "AEE", "MKC", "COO",
    "SWKS", "AKAM", "BAX", "RF", "STE", "CHRW", "HII", "NDAQ", "JBHT",
    "STT", "ESS", "CAG", "WAT", "JKHY", "IPG", "TECH", "PKI", "MOS", "GEN",
    "NRG", "HOLX", "MKTX", "ZION", "FMC", "NDSN", "BIO", "VTRS", "TER",
    "WRB", "BEN", "GRMN", "BBY", "DHI", "TXT", "PFG", "TPR", "HSIC",
    "LNT", "CPB", "ROL", "NI", "K", "IRM", "PNW", "AIZ", "HWM", "WHR"
]

seen_flips = {}

def get_bars(symbol):
    end = datetime.utcnow()
    start = end - timedelta(days=100)
    request = StockBarsRequest(
        symbol_or_symbols=symbol,
        timeframe=TimeFrame.Day,
        start=start,
        end=end,
        feed='iex'
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

