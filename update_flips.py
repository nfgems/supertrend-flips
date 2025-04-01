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
        if isinstance(flips, list) and all(
            isinstance(entry, dict) and "date" in entry and "type" in entry
            for entry in flips
        ):
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

def get_bars(symbol, retries=3, delay=3, timeframe=TimeFrame.Day):
    end = datetime.utcnow()
    start = end - timedelta(days=1000)
    request = StockBarsRequest(
        symbol_or_symbols=symbol,
        timeframe=timeframe,
        start=start,
        end=end,
        feed='iex'
    )
    for attempt in range(retries):
        try:
            bars = client.get_stock_bars(request).df

            if bars.empty:
                logger.warning(f"{symbol} - No data returned from Alpaca.")
                return None

            if isinstance(bars.index, pd.MultiIndex):
                if symbol not in bars.index.levels[0]:
                    logger.warning(f"{symbol} - Not found in multi-indexed response.")
                    return None
                bars = bars.xs(symbol, level=0)

            return bars

        except Exception as e:
            logger.warning(f"{symbol} - Retry {attempt + 1}/{retries}: {e}")
            time.sleep(delay)

    logger.error(f"{symbol} - Failed after {retries} retries.")
    return None

def calculate_supertrend(df):
    st = ta.supertrend(df['high'], df['low'], df['close'], length=10, multiplier=3.0)
    return df.join(st)

def detect_flips(df, symbol, existing):
    if 'SUPERT_10_3.0' not in df.columns:
        logger.warning(f"{symbol} missing Supertrend column. Skipping.")
        return

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

    all_flips = flips + new_flips
    all_flips.sort(key=lambda x: x["date"], reverse=True)
    existing[symbol] = all_flips

def run_for_timeframe(label, timeframe):
    filename = f"public_flips_{label}.json"
    flip_data = load_flip_history(filename)

    for symbol in SP500:
        try:
            df = get_bars(symbol, timeframe=timeframe)
            if df is None or len(df) < 6:
                logger.warning(f"{symbol} - No data returned or insufficient candles.")
                continue

            df = calculate_supertrend(df)
            detect_flips(df, symbol, flip_data)

        except Exception as e:
            logger.error(f"{symbol} - Unexpected error: {e}")

    save_flip_history(flip_data, filename)
    logger.info(f"✅ {label.upper()} flip detection complete. {filename} updated.")

if __name__ == "__main__":
    for label, tf in TIMEFRAMES.items():
        run_for_timeframe(label, tf)
