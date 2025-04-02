import pandas as pd
import pandas_ta as ta
import requests
import random
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
    "A", "AAPL", "ABBV", "ABNB", "ABT", "ACAD", "ACGL", "ACN", "ADBE", "ADI", "ADM", "ADP", "ADSK", "AEE", "AEP", "AES", "AFL", "AFRM", "AIG", "AIZ", "AJG", "AKAM", "ALB", "ALGN", "ALL", "ALLE", "ALLY", "ALNY", "AMAT", "AMCR", "AMD", "AME", "AMGN", "AMP", "AMT", "AMZN", "ANET", "ANSS", "AON", "AOS", "APA", "APD", "APH", "APO", "APPF", "APPN", "APTV", "ARLO", "ARE", "ATO", "AVAV", "AVB", "AVGO", "AVY", "AWK", "AXON", "AXP", "AZO",
    "BA", "BAC", "BALL", "BAX", "BBY", "BDX", "BEN", "BF.B", "BG", "BIIB", "BKR", "BMBL", "BMY", "BR", "BRK.B", "BRO", "BSX", "BWXT", "BX", "BXP",
    "C", "CAG", "CAH", "CARR", "CAT", "CB", "CBOE", "CBRE", "CCI", "CCL", "CDNS", "CDW", "CEG", "CF", "CFG", "CHD", "CHRW", "CHTR", "CHWY", "CI", "CINF", "CIVI", "CL", "CLX", "CMCSA", "CMA", "CME", "CMG", "CMI", "CMS", "CNC", "CNP", "COF", "COIN", "COO", "COP", "COST", "CPB", "CPAY", "CPRT", "CPT", "CRL", "CRM", "CRWD", "CSCO", "CSGP", "CSX", "CTAS", "CTRA", "CTSH", "CTVA", "CUBI", "CVS", "CVX", "CW", "CZR",
    "D", "DAL", "DASH", "DD", "DE", "DECK", "DELL", "DFS", "DG", "DGX", "DHI", "DHR", "DIS", "DLR", "DLTR", "DNA", "DOC", "DOV", "DOW", "DPZ", "DRI", "DTE", "DUK", "DVN", "DVA", "DXCM",
    "EA", "EBAY", "ECL", "ED", "EFX", "EG", "EIX", "EL", "ELV", "EMN", "EMR", "ENPH", "ENVX", "EOG", "EPAM", "EQIX", "EQR", "EQT", "ES", "ESS", "ETN", "ETR", "EVGO", "EVRG", "EXC", "EXEL", "EXPD", "EXPE", "EXR",
    "F", "FANG", "FAST", "FCX", "FDS", "FDX", "FE", "FFIV", "FHN", "FI", "FICO", "FIS", "FITB", "FRT", "FSLR", "FUBO", "FTNT", "FTV",
    "GD", "GDDY", "GE", "GEHC", "GEN", "GENI", "GILD", "GIS", "GL", "GLW", "GM", "GNRC", "GOOG", "GOOGL", "GPC", "GPN", "GRMN", "GRND", "GS", "GTLB", "GWW",
    "HAL", "HAS", "HBAN", "HBNC", "HCA", "HD", "HES", "HIG", "HII", "HIMS", "HLX", "HLT", "HOLX", "HON", "HOOD", "HPE", "HPQ", "HRL", "HSIC", "HST", "HSY", "HUBB", "HUBC", "HUM", "HWM", "HXL",
    "IBM", "ICE", "IDXX", "IEX", "IFF", "INCY", "INTC", "INTU", "INVH", "IP", "IPG", "IQV", "IR", "IRM", "ISRG", "IT", "ITW", "IVZ",
    "J", "JBHT", "JBL", "JCI", "JKHY", "JNJ", "JNPR", "JOBY", "JPM",
    "K", "KDP", "KEY", "KEYS", "KHC", "KIM", "KKR", "KLAC", "KMB", "KMI", "KMX", "KO", "KR", "KTOS", "KVUE",
    "L", "LC", "LDOS", "LEN", "LH", "LHX", "LI", "LII", "LIN", "LKQ", "LLY", "LMND", "LMT", "LNT", "LOW", "LRCX", "LULU", "LUV", "LVS", "LW", "LZ", "LYB", "LYV",
    "MA", "MAA", "MAR", "MARA", "MAS", "MCD", "MCHP", "MCK", "MCO", "MDLZ", "MDT", "META", "MET", "MGM", "MHK", "MKC", "MKL", "MKTX", "MLM", "MMM", "MNST", "MO", "MOH", "MOS", "MPC", "MPWR", "MRK", "MRNA", "MSTR", "MS", "MSCI", "MSFT", "MSI", "MTB", "MTCH", "MTDR", "MTD", "MU", "NBIX", "NCLH", "NDAQ", "NDSN", "NEE", "NEM", "NFLX", "NI", "NIO", "NKE", "NOC", "NOW", "NRG", "NSC", "NTAP", "NTRS", "NU", "NUE", "NVDA", "NVR", "NWS", "NWSA", "NXPI",
    "O", "ODFL", "OKE", "OMC", "ON", "ONON", "OPEN", "ORCL", "ORCL", "ORI", "ORLY", "OTIS", "OXY",
    "PANW", "PARA", "PARR", "PATH", "PAYC", "PAYX", "PB", "PCAR", "PCG", "PEG", "PEP", "PFE", "PFG", "PG", "PGR", "PH", "PHM", "PKG", "PLD", "PLTR", "PM", "PNC", "PNR", "PNW", "PODD", "POOL", "PPG", "PPL", "PRCH", "PRU", "PSA", "PSX", "PTC", "PWR", "PYPL",
    "QCOM", "QS",
    "RBLX", "RCL", "REG", "REGN", "RF", "RIVN", "RJF", "RL", "RMD", "ROK", "ROL", "ROP", "ROKU", "ROST", "RNR", "RSG", "RTX", "RVTY",
    "SBAC", "SBUX", "SCHW", "SDGR", "SHW", "SIRI", "SJM", "SLB", "SM", "SMCI", "SNA", "SNPS", "SO", "SOFI", "SOUN", "SPG", "SPGI", "SRE", "STE", "STLD", "STT", "STX", "STZ", "SWK", "SWKS", "SYF", "SYK", "SYY",
    "T", "TALO", "TAP", "TDG", "TDY", "TECH", "TEL", "TER", "TFC", "TGT", "THG", "TJX", "TMDX", "TMO", "TMUS", "TPR", "TRGP", "TRMB", "TROW", "TRUP", "TRV", "TSCO", "TSLA", "TSN", "TTOO", "TT", "TTWO", "TXN", "TXT", "TYL",
    "UAL", "UDR", "UHS", "ULTA", "UNH", "UNP", "UPST", "UPWK", "UPS", "URI", "USB",
    "V", "VFS", "VICI", "VLO", "VLTO", "VMC", "VRSK", "VRSN", "VRTX", "VST", "VTR", "VTRS", "VTLE", "VZ",
    "WAB", "WAL", "WAT", "WBA", "WBD", "WDAY", "WDC", "WEC", "WELL", "WFC", "WHR", "WM", "WMB", "WMT", "WRB", "WSM", "WST", "WTW", "WY", "WYNN",
    "XEL", "XOM", "XPEV", "XYL",
    "YUM",
    "ZBH", "ZBRA", "ZTS"
]

CRYPTO_SYMBOLS = {
    "BTC": "BTCUSDT",
    "ETH": "ETHUSDT",
    "BNB": "BNBUSDT",
    "SOL": "SOLUSDT",
    "XRP": "XRPUSDT",
    "LINK": "LINKUSDT",
    "DOGE": "DOGEUSDT",
    "ADA": "ADAUSDT",
    "TRX": "TRXUSDT",
    "AVAX": "AVAXUSDT",
    "SUI": "SUIUSDT",
    "LTC": "LTCUSDT",
    "BCH": "BCHUSDT",
    "APT": "APTUSDT",
    "PEPE": "PEPEUSDT",
    "TAO": "TAOUSDT",
    "ENA": "ENAUSDT",
    "TRUMP": "TRUMPUSDT",
    "AAVE": "AAVEUSDT",
    "BONK": "BONKUSDT",
    "WIF": "WIFUSDT",
    "PENGU": "PENGUUSDT",
    "POPCAT": "POPCATUSDT",
    "MELANIA": "MELANIAUSDT",
    "SONIC": "SUSDC"
}

CRYPTO = list(CRYPTO_SYMBOLS.keys())

TIMEFRAMES = {
    "1d": TimeFrame.Day,
    "1w": TimeFrame.Week,
    "1m": TimeFrame.Month
}

def load_flip_history(filename):
    if not os.path.exists(filename):
        return {}
    with open(filename, "r") as f:
        raw_data = json.load(f)
    cleaned = {}
    for symbol, flips in raw_data.items():
        if isinstance(flips, list) and all(isinstance(entry, dict) and "date" in entry and "type" in entry for entry in flips):
            cleaned[symbol] = flips
        else:
            logger.warning(f"{symbol} had malformed flip data. Resetting.")
            cleaned[symbol] = []
    with open(filename, "w") as f:
        json.dump(cleaned, f, indent=2)
    return cleaned

def save_flip_history(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

def get_crypto_ohlc(symbol, interval="1d", limit=365, retries=3, delay=3):
    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    for attempt in range(retries):
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            raw = response.json()
            if not raw:
                return None
            df = pd.DataFrame(raw, columns=[
                "timestamp", "open", "high", "low", "close", "volume",
                "close_time", "quote_asset_volume", "number_of_trades",
                "taker_buy_base_vol", "taker_buy_quote_vol", "ignore"
            ])
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
            df.set_index("timestamp", inplace=True)
            df["high"] = pd.to_numeric(df["high"])
            df["low"] = pd.to_numeric(df["low"])
            df["close"] = pd.to_numeric(df["close"])
            return df[["high", "low", "close"]]
        except requests.exceptions.HTTPError as e:
            status = e.response.status_code if e.response else "Unknown"
            logger.warning(f"{symbol} - HTTP error {status}: {e}")
            if status == 429:
                logger.warning(f"{symbol} - Rate limited. Retrying in {delay}s...")
                time.sleep(delay)
        except Exception as e:
            logger.warning(f"{symbol} - Unexpected error: {e}")
            time.sleep(delay)
    return None

def calculate_supertrend(df):
    st = ta.supertrend(df['high'], df['low'], df['close'], length=10, multiplier=3.0)
    return df.join(st)

def detect_flips(df, display_symbol, existing):
    if 'SUPERT_10_3.0' not in df.columns:
        logger.warning(f"{display_symbol} missing Supertrend column. Skipping.")
        return
    flips = existing.get(display_symbol, [])
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
    all_flips = flips + new_flips
    all_flips.sort(key=lambda x: x["date"], reverse=True)
    existing[display_symbol] = all_flips

def run_crypto():
    filename = "public_flips_crypto.json"
    flip_data = load_flip_history(filename)
    for display_symbol in CRYPTO:
        binance_symbol = CRYPTO_SYMBOLS[display_symbol]
        df = get_crypto_ohlc(binance_symbol)
        if df is None or len(df) < 6:
            logger.warning(f"{display_symbol} - Not enough data for flip detection.")
            continue
        df = calculate_supertrend(df)
        detect_flips(df, display_symbol, flip_data)
        time.sleep(3 + random.uniform(0.5, 1.5))
    save_flip_history(flip_data, filename)
    logger.info(f"✅ CRYPTO flip detection complete. {filename} updated.")

def run_stocks():
    for label, tf in TIMEFRAMES.items():
        filename = f"public_flips_{label}.json"
        flip_data = load_flip_history(filename)
        for symbol in SP500:
            try:
                end = datetime.utcnow()
                start = end - timedelta(days=1000)
                request = StockBarsRequest(
                    symbol_or_symbols=symbol,
                    timeframe=tf,
                    start=start,
                    end=end,
                    feed='iex'
                )
                bars = client.get_stock_bars(request).df
                if bars.empty or len(bars) < 6:
                    logger.warning(f"{symbol} - No data or insufficient candles.")
                    continue
                if isinstance(bars.index, pd.MultiIndex):
                    if symbol not in bars.index.levels[0]:
                        logger.warning(f"{symbol} - Not found in multi-indexed response.")
                        continue
                    bars = bars.xs(symbol, level=0)
                bars = calculate_supertrend(bars)
                detect_flips(bars, symbol, flip_data)
            except Exception as e:
                logger.error(f"{symbol} - Error during stock processing: {e}")
        save_flip_history(flip_data, filename)
        logger.info(f"✅ {label.upper()} stock flip detection complete. {filename} updated.")

if __name__ == "__main__":
    run_stocks()
    run_crypto()
