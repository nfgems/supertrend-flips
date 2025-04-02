import pandas as pd
import pandas_ta as ta
import yfinance as yf
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

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("flips.log"), logging.StreamHandler()]
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
    "BTC": "BTC-USD",
    "ETH": "ETH-USD",
    "SOL": "SOL-USD",
    "XRP": "XRP-USD",
    "LINK": "LINK-USD",
    "DOGE": "DOGE-USD",
    "ADA": "ADA-USD",
    "AVAX": "AVAX-USD",
    "SUI": "SUI-USD",
    "LTC": "LTC-USD",
    "BCH": "BCH-USD",
    "APT": "APT-USD",
    "PEPE": "PEPE-USD",
    "TAO": "TAO-USD",
    "TRUMP": "TRUMP-USD",
    "AAVE": "AAVE-USD",
    "BONK": "BONK-USD",
    "WIF": "WIF-USD",
    "PENGU": "PENGU-USD",
    "POPCAT": "POPCAT-USD",
    "00": "00-USD",
    "1INCH": "1INCH-USD",
    "A8": "A8-USD",
    "ABT": "ABT-USD",
    "ACH": "ACH-USD",
    "ACS": "ACS-USD",
    "ACX": "ACX-USD",
    "AERGO": "AERGO-USD",
    "AERO": "AERO-USD",
    "AGLD": "AGLD-USD",
    "AIOZ": "AIOZ-USD",
    "AKT": "AKT-USD",
    "ALCX": "ALCX-USD",
    "ALEO": "ALEO-USD",
    "ALEPH": "ALEPH-USD",
    "ALGO": "ALGO-USD",
    "ALICE": "ALICE-USD",
    "ALT": "ALT-USD",
    "AMP": "AMP-USD",
    "ANKR": "ANKR-USD",
    "APE": "APE-USD",
    "API3": "API3-USD",
    "ARB": "ARB-USD",
    "ARKM": "ARKM-USD",
    "ARPA": "ARPA-USD",
    "ASM": "ASM-USD",
    "AST": "AST-USD",
    "ATH": "ATH-USD",
    "ATOM": "ATOM-USD",
    "AUCTION": "AUCTION-USD",
    "AUDIO": "AUDIO-USD",
    "AURORA": "AURORA-USD",
    "AVT": "AVT-USD",
    "AXL": "AXL-USD",
    "AXS": "AXS-USD",
    "B3": "B3-USD",
    "BADGER": "BADGER-USD",
    "BAL": "BAL-USD",
    "BAND": "BAND-USD",
    "BAT": "BAT-USD",
    "BERA": "BERA-USD",
    "BICO": "BICO-USD",
    "BIGTIME": "BIGTIME-USD",
    "BLAST": "BLAST-USD",
    "BLUR": "BLUR-USD",
    "BLZ": "BLZ-USD",
    "BNT": "BNT-USD",
    "BOBA": "BOBA-USD",
    "BTRST": "BTRST-USD",
    "C98": "C98-USD",
    "CBETH": "CBETH-USD",
    "CELR": "CELR-USD",
    "CGLD": "CGLD-USD",
    "CHZ": "CHZ-USD",
    "CLV": "CLV-USD",
    "COMP": "COMP-USD",
    "COOKIE": "COOKIE-USD",
    "CORECHAIN": "CORECHAIN-USD",
    "COTI": "COTI-USD",
    "COW": "COW-USD",
    "CRO": "CRO-USD",
    "CRV": "CRV-USD",
    "CTSI": "CTSI-USD",
    "CTX": "CTX-USD",
    "CVC": "CVC-USD",
    "CVX": "CVX-USD",
    "DAI": "DAI-USD",
    "DAR": "DAR-USD",
    "DASH": "DASH-USD",
    "DEGEN": "DEGEN-USD",
    "DEXT": "DEXT-USD",
    "DIA": "DIA-USD",
    "DIMO": "DIMO-USD",
    "DNT": "DNT-USD",
    "DOGINME": "DOGINME-USD",
    "DOT": "DOT-USD",
    "DRIFT": "DRIFT-USD",
    "EGLD": "EGLD-USD",
    "EIGEN": "EIGEN-USD",
    "ELA": "ELA-USD",
    "ENS": "ENS-USD",
    "EOS": "EOS-USD",
    "ERN": "ERN-USD",
    "ETC": "ETC-USD",
    "ETHFI": "ETHFI-USD",
    "FAI": "FAI-USD",
    "FARM": "FARM-USD",
    "FET": "FET-USD",
    "FIDA": "FIDA-USD",
    "FIL": "FIL-USD",
    "FIS": "FIS-USD",
    "FLOKI": "FLOKI-USD",
    "FLOW": "FLOW-USD",
    "FLR": "FLR-USD",
    "FORT": "FORT-USD",
    "FORTH": "FORTH-USD",
    "FOX": "FOX-USD",
    "FX": "FX-USD",
    "G": "G-USD",
    "GAL": "GAL-USD",
    "GFI": "GFI-USD",
    "GHST": "GHST-USD",
    "GIGA": "GIGA-USD",
    "GLM": "GLM-USD",
    "GMT": "GMT-USD",
    "GNO": "GNO-USD",
    "GODS": "GODS-USD",
    "GRT": "GRT-USD",
    "GST": "GST-USD",
    "GTC": "GTC-USD",
    "GUSD": "GUSD-USD",
    "GYEN": "GYEN-USD",
    "HBAR": "HBAR-USD",
    "HFT": "HFT-USD",
    "HIGH": "HIGH-USD",
    "HNT": "HNT-USD",
    "HONEY": "HONEY-USD",
    "HOPR": "HOPR-USD",
    "ICP": "ICP-USD",
    "IDEX": "IDEX-USD",
    "ILV": "ILV-USD",
    "IMX": "IMX-USD",
    "INDEX": "INDEX-USD",
    "INJ": "INJ-USD",
    "INV": "INV-USD",
    "IO": "IO-USD",
    "IOTX": "IOTX-USD",
    "IP": "IP-USD",
    "JASMY": "JASMY-USD",
    "JTO": "JTO-USD",
    "KAITO": "KAITO-USD",
    "KARRAT": "KARRAT-USD",
    "KAVA": "KAVA-USD",
    "KEYCAT": "KEYCAT-USD",
    "KNC": "KNC-USD",
    "KRL": "KRL-USD",
    "KSM": "KSM-USD",
    "LCX": "LCX-USD",
    "LDO": "LDO-USD",
    "LIT": "LIT-USD",
    "LOKA": "LOKA-USD",
    "LPT": "LPT-USD",
    "LQTY": "LQTY-USD",
    "LRC": "LRC-USD",
    "LRDS": "LRDS-USD",
    "LSETH": "LSETH-USD",
    "MAGIC": "MAGIC-USD",
    "MANA": "MANA-USD",
    "MASK": "MASK-USD",
    "MATH": "MATH-USD",
    "MATIC": "MATIC-USD",
    "MDT": "MDT-USD",
    "ME": "ME-USD",
    "MEDIA": "MEDIA-USD",
    "METIS": "METIS-USD",
    "MINA": "MINA-USD",
    "MKR": "MKR-USD",
    "MLN": "MLN-USD",
    "MNDE": "MNDE-USD",
    "MOBILE": "MOBILE-USD",
    "MOG": "MOG-USD",
    "MOODENG": "MOODENG-USD",
    "MORPHO": "MORPHO-USD",
    "MOVE": "MOVE-USD",
    "MPL": "MPL-USD",
    "MSOL": "MSOL-USD",
    "MUSE": "MUSE-USD",
    "NCT": "NCT-USD",
    "NEAR": "NEAR-USD",
    "NEON": "NEON-USD",
    "NKN": "NKN-USD",
    "NMR": "NMR-USD",
    "OCEAN": "OCEAN-USD",
    "OGN": "OGN-USD",
    "OMNI": "OMNI-USD",
    "ONDO": "ONDO-USD",
    "OP": "OP-USD",
    "ORCA": "ORCA-USD",
    "ORN": "ORN-USD",
    "OSMO": "OSMO-USD",
    "OXT": "OXT-USD",
    "PAX": "PAX-USD",
    "PENDLE": "PENDLE-USD",
    "PERP": "PERP-USD",
    "PIRATE": "PIRATE-USD",
    "PLU": "PLU-USD",
    "PNG": "PNG-USD",
    "PNUT": "PNUT-USD",
    "POL": "POL-USD",
    "POLS": "POLS-USD",
    "POND": "POND-USD",
    "POWR": "POWR-USD",
    "PRCL": "PRCL-USD",
    "PRIME": "PRIME-USD",
    "PRO": "PRO-USD",
    "PRQ": "PRQ-USD",
    "PUNDIX": "PUNDIX-USD",
    "PYR": "PYR-USD",
    "PYTH": "PYTH-USD",
    "PYUSD": "PYUSD-USD",
    "QI": "QI-USD",
    "QNT": "QNT-USD",
    "RAD": "RAD-USD",
    "RARE": "RARE-USD",
    "RARI": "RARI-USD",
    "RBN": "RBN-USD",
    "RED": "RED-USD",
    "RENDER": "RENDER-USD",
    "REQ": "REQ-USD",
    "REZ": "REZ-USD",
    "RLC": "RLC-USD",
    "RNDR": "RNDR-USD",
    "RONIN": "RONIN-USD",
    "ROSE": "ROSE-USD",
    "RPL": "RPL-USD",
    "SAFE": "SAFE-USD",
    "SAND": "SAND-USD",
    "SD": "SD-USD",
    "SEAM": "SEAM-USD",
    "SEI": "SEI-USD",
    "SHDW": "SHDW-USD",
    "SHIB": "SHIB-USD",
    "SHPING": "SHPING-USD",
    "SKL": "SKL-USD",
    "SNX": "SNX-USD",
    "SPA": "SPA-USD",
    "SPELL": "SPELL-USD",
    "STG": "STG-USD",
    "STORJ": "STORJ-USD",
    "STRK": "STRK-USD",
    "STX": "STX-USD",
    "SUKU": "SUKU-USD",
    "SUPER": "SUPER-USD",
    "SUSHI": "SUSHI-USD",
    "SWELL": "SWELL-USD",
    "SWFTC": "SWFTC-USD",
    "SYN": "SYN-USD",
    "SYRUP": "SYRUP-USD",
    "T": "T-USD",
    "TIA": "TIA-USD",
    "TIME": "TIME-USD",
    "TNSR": "TNSR-USD",
    "TOSHI": "TOSHI-USD",
    "TRAC": "TRAC-USD",
    "TRB": "TRB-USD",
    "TRU": "TRU-USD",
    "TURBO": "TURBO-USD",
    "UMA": "UMA-USD",
    "UNI": "UNI-USD",
    "USDT": "USDT-USD",
    "VARA": "VARA-USD",
    "VELO": "VELO-USD",
    "VET": "VET-USD",
    "VOXEL": "VOXEL-USD",
    "VTHO": "VTHO-USD",
    "VVV": "VVV-USD",
    "WAXL": "WAXL-USD",
    "WCFG": "WCFG-USD",
    "WELL": "WELL-USD",
    "XCN": "XCN-USD",
    "XLM": "XLM-USD",
    "XTZ": "XTZ-USD",
    "XYO": "XYO-USD",
    "YFI": "YFI-USD",
    "ZEC": "ZEC-USD",
    "ZEN": "ZEN-USD",
    "ZETA": "ZETA-USD",
    "ZETACHAIN": "ZETACHAIN-USD",
    "ZK": "ZK-USD",
    "ZRO": "ZRO-USD",
    "ZRX": "ZRX-USD"
}

CRYPTO = list(CRYPTO_SYMBOLS.keys())

TIMEFRAMES = {
    "1d": TimeFrame.Day,
    "1w": TimeFrame.Week,
    "1m": TimeFrame.Month
}

COINBASE_GRANULARITIES = {
    "1d": 86400
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

def get_crypto_ohlc(symbol, timeframe="1d", retries=3, delay=3):
    url = f"https://api.exchange.coinbase.com/products/{symbol}/candles"
    params = {
        "granularity": COINBASE_GRANULARITIES[timeframe],
        "limit": 365
    }
    for attempt in range(retries):
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            raw = response.json()
            if not raw:
                return None
            df = pd.DataFrame(raw, columns=["time", "low", "high", "open", "close", "volume"])
            df["timestamp"] = pd.to_datetime(df["time"], unit="s")
            df.set_index("timestamp", inplace=True)
            df = df.sort_index()
            return df[["high", "low", "close"]]
        except Exception as e:
            logger.warning(f"{symbol} - Error fetching crypto OHLC: {e}")
            time.sleep(delay)
    return None

def get_stock_ohlc(symbol, label, retries=3, delay=1):
    for attempt in range(retries):
        try:
            if label == "1d":
                end = datetime.utcnow()
                start = end - timedelta(days=365)
                bars = client.get_stock_bars(StockBarsRequest(symbol_or_symbols=symbol, start=start, end=end, timeframe=TimeFrame.Day))
                df = bars.df
                if df.empty:
                    return None
                df = df[df.index.get_level_values(0) == symbol]
                df = df.sort_index()
                return df[["high", "low", "close"]]
            else:
                interval = "1wk" if label == "1w" else "1mo"
                df = yf.download(symbol, period="1y", interval=interval, progress=False)
                if df.empty or df.isnull().all().all():
                    return None
                df.index.name = "timestamp"
                df = df[["High", "Low", "Close"]].rename(columns={"High": "high", "Low": "low", "Close": "close"})
                df = df.dropna()
                return df
        except Exception as e:
            logger.warning(f"{symbol} ({label}) - Attempt {attempt+1} error: {e}")
            time.sleep(delay)
    return None

def calculate_supertrend(df):
    try:
        st = ta.supertrend(df['high'], df['low'], df['close'], length=10, multiplier=3.0)
        if st is None or st.empty:
            return None
        return df.join(st)
    except Exception as e:
        logger.warning(f"Supertrend calculation failed: {e}")
        return None

def detect_flips(df, display_symbol, existing):
    if 'SUPERT_10_3.0' not in df.columns:
        logger.warning(f"{display_symbol} missing Supertrend column. Skipping.")
        return
    flips = existing.get(display_symbol, [])
    recorded_dates = set((entry["date"], entry["type"]) for entry in flips)
    new_flips = []
    for i in range(1, len(df)):
        prev = df.iloc[i - 1]
        curr = df.iloc[i]
        date_str = str(curr.name.date())
        if (date_str, "green") in recorded_dates or (date_str, "red") in recorded_dates:
            continue
        if prev['SUPERT_10_3.0'] > prev['close'] and curr['SUPERT_10_3.0'] < curr['close']:
            new_flips.append({"date": date_str, "type": "green"})
        elif prev['SUPERT_10_3.0'] < prev['close'] and curr['SUPERT_10_3.0'] > curr['close']:
            new_flips.append({"date": date_str, "type": "red"})
    if new_flips:
        all_flips = flips + new_flips
        all_flips.sort(key=lambda x: x["date"], reverse=True)
        existing[display_symbol] = all_flips

def run_stocks():
    for label in TIMEFRAMES:
        filename = f"public_flips_{label}.json"
        flip_data = load_flip_history(filename)

        for display_symbol in SP500:
            logger.info(f"📈 Processing {display_symbol} ({label})")
            df = get_stock_ohlc(display_symbol, label)
            if df is None or len(df) < 6:
                logger.warning(f"{display_symbol} ({label}) - Not enough data.")
                continue

            df = calculate_supertrend(df)
            if df is None:
                logger.warning(f"{display_symbol} ({label}) - Supertrend failed.")
                continue

            before = len(flip_data.get(display_symbol, []))
            detect_flips(df, display_symbol, flip_data)
            after = len(flip_data.get(display_symbol, []))
            logger.info(f"{display_symbol} ({label}) - {after - before} new flips.")

            if label in ["1w", "1m"]:
                time.sleep(1.5 + random.uniform(0.5, 1.0))
            else:
                time.sleep(0.5)

        save_flip_history(flip_data, filename)
        logger.info(f"✅ STOCKS flip detection complete for {label.upper()} timeframe.")

def run_crypto():
    for label in COINBASE_GRANULARITIES.keys():
        filename = f"public_flips_crypto_{label}.json"
        flip_data = load_flip_history(filename)

        for display_symbol in CRYPTO:
            logger.info(f"🔍 Processing {display_symbol} ({label})")
            cb_symbol = CRYPTO_SYMBOLS[display_symbol]
            df = get_crypto_ohlc(cb_symbol, timeframe=label)
            if df is None or len(df) < 6:
                logger.warning(f"{display_symbol} ({label}) - Not enough data.")
                continue
            df = calculate_supertrend(df)
            if df is None:
                logger.warning(f"{display_symbol} ({label}) - Supertrend failed.")
                continue
            before = len(flip_data.get(display_symbol, []))
            detect_flips(df, display_symbol, flip_data)
            after = len(flip_data.get(display_symbol, []))
            logger.info(f"{display_symbol} ({label}) - {after - before} new flips.")
            time.sleep(1.5 + random.uniform(0.5, 1.0))

        save_flip_history(flip_data, filename)
        logger.info(f"✅ CRYPTO flip detection complete for {label.upper()} timeframe.")

if __name__ == "__main__":
    run_stocks()
    run_crypto()
