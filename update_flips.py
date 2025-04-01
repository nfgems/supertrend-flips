import pandas as pd
import pandas_ta as ta
from alpaca.data.historical.stock import StockHistoricalDataClient 
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime, timedelta
import os
import json
import time
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("flips.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger()

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
    "LNT", "CPB", "ROL", "NI", "K", "IRM", "PNW", "AIZ", "HWM", "WHR",
    "MSTR", "COIN", "GRND", "HOOD", "BRPHF", "PLTR", "NIO", "LCID", "SOFI", "ROKU",
    "AFRM", "CHWY", "RIVN", "FUBO", "OPEN", "UPST", "DKNG", "RBLX", "ENVX", "SOUN",
    "BMBL", "GENI", "NU", "GTLB", "PATH", "DNA", "SIRI", "AI", "HIMS", "XPEV",
    "LI", "JOBY", "EVGO", "QS", "QSAM", "ASTR", "RKLB", "VFS", "LC", "UPWK",
    "TTOO", "TMDX", "ONON", "LZ", "SDGR", "SMCI", "HUBC", "WBD", "PRCH", "ARLO",
    "LMND", "TRUP", "ACGL", "RNR", "MKL", "THG", "AGO", "ORI",
    "GD", "CW", "KTOS", "AVAV", "BWXT", "AXON", "HXL",
    "SGEN", "NBIX", "ALNY", "BMRN", "INCY", "ACAD", "EXEL",
    "ALLY", "FHN", "CMA", "HBNC", "PB", "SIVBQ", "WAL", "CUBI",
    "APA", "MTDR", "PARR", "TALO", "SM", "VTLE", "CPE", "CIVI", "PDCE"
]

def load_flip_history():
    if os.path.exists("public_flips.json"):
        with open("public_flips.json", "r") as f:
            return json.load(f)
    return {}

def save_flip_history(data):
    with open("public_flips.json", "w") as f:
        json.dump(data, f, indent=2)

def get_bars(symbol, retries=3, delay=3):
    end = datetime.utcnow()
    start = end - timedelta(days=100)
    request = StockBarsRequest(
        symbol_or_symbols=symbol,
        timeframe=TimeFrame.Day,
        start=start,
        end=end,
        feed='iex'
    )
    for attempt in range(retries):
        try:
            bars = client.get_stock_bars(request).df
            if bars.empty or symbol not in bars.index.levels[0]:
                return None
            return bars.xs(symbol, level=0)
        except Exception as e:
            logger.warning(f"Retry {attempt + 1}/{retries} for {symbol}: {e}")
            time.sleep(delay)
    logger.error(f"Failed to fetch bars for {symbol} after {retries} retries.")
    return None

def calculate_supertrend(df):
    st = ta.supertrend(df['high'], df['low'], df['close'], length=10, multiplier=3.0)
    return df.join(st)

def detect_flips(df, symbol, existing):
    flips = existing.get(symbol, [])
    recorded_dates = {entry["date"] for entry in flips}
    new_flips = []

    for i in range(1, len(df)):
        prev = df.iloc[i - 1]
        curr = df.iloc[i]
        date_str = str(curr.name.date())

        if date_str in recorded_dates:
            continue

        if prev['SUPERT_10_3.0'] > prev['close'] and curr['SUPERT_10_3.0'] < curr['close']:
            new_flips.append({"date": date_str, "type": "green"})
        elif prev['SUPERT_10_3.0'] < prev['close'] and curr['SUPERT_10_3.0'] > curr['close']:
            new_flips.append({"date": date_str, "type": "red"})

    if new_flips:
        flips.extend(new_flips)
        flips.sort(key=lambda x: x["date"], reverse=True)
        existing[symbol] = flips

def scan():
    flip_data = load_flip_history()

    for symbol in SP500:
        try:
            df = get_bars(symbol)
            if df is None or len(df) < 6:
                continue
            df = calculate_supertrend(df)
            detect_flips(df, symbol, flip_data)
        except Exception as e:
            logger.error(f"{symbol} error: {e}")

    save_flip_history(flip_data)

if __name__ == "__main__":
    scan()
