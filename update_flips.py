import pandas as pd
import pandas_ta as ta
import yfinance as yf
import requests
import random
from kucoin.client import Client  
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
kucoin_client = Client()  


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
    "O", "ODFL", "OKE", "OMC", "ON", "ONON", "OPEN", "BLK", "ORCL", "ORI", "ORLY", "OTIS", "OXY",
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

# Create a set of tickers to help avoid duplicates
SP500_SET = set(SP500)

CRYPTO_SYMBOLS = {
    "1CAT": "1CAT-USD",
    "1INCH": "1INCH-USD",
    "AA": "AA-USD",
    "AAVE": "AAVE-USD",
    "AAVE3L": "AAVE3L-USD",
    "AAVE3S": "AAVE3S-USD",
    "ACE": "ACE-USD",
    "ACH": "ACH-USD",
    "ACQ": "ACQ-USD",
    "ACS": "ACS-USD",
    "ACTSOL": "ACTSOL-USD",
    "ACX": "ACX-USD",
    "ADA": "ADA-USD",
    "ADA3L": "ADA3L-USD",
    "ADA3S": "ADA3S-USD",
    "ADS": "ADS-USD",
    "ADX": "ADX-USD",
    "AEG": "AEG-USD",
    "AERGO": "AERGO-USD",
    "AERO": "AERO-USD",
    "AEVO": "AEVO-USD",
    "AFG": "AFG-USD",
    "AGLD": "AGLD-USD",
    "AI16Z": "AI16Z-USD",
    "AIEPK": "AIEPK-USD",
    "AIOZ": "AIOZ-USD",
    "AIPAD": "AIPAD-USD",
    "AIPUMP": "AIPUMP-USD",
    "AITECH": "AITECH-USD",
    "AIXBT": "AIXBT-USD",
    "AKT": "AKT-USD",
    "ALEPH": "ALEPH-USD",
    "ALEX": "ALEX-USD",
    "ALGO": "ALGO-USD",
    "ALICE": "ALICE-USD",
    "ALPHA": "ALPHA-USD",
    "ALPINE": "ALPINE-USD",
    "ALU": "ALU-USD",
    "AMB": "AMB-USD",
    "AMP": "AMP-USD",
    "AMPL": "AMPL-USD",
    "AMU": "AMU-USD",
    "ANALOS": "ANALOS-USD",
    "ANIME": "ANIME-USD",
    "ANKR": "ANKR-USD",
    "ANLOG": "ANLOG-USD",
    "ANYONE": "ANYONE-USD",
    "AOG": "AOG-USD",
    "APE": "APE-USD",
    "APE3L": "APE3L-USD",
    "APE3S": "APE3S-USD",
    "API3": "API3-USD",
    "APP": "APP-USD",
    "APT": "APT-USD",
    "AR": "AR-USD",
    "ARB": "ARB-USD",
    "ARB3L": "ARB3L-USD",
    "ARB3S": "ARB3S-USD",
    "ARC": "ARC-USD",
    "ARCA": "ARCA-USD",
    "ARCSOL": "ARCSOL-USD",
    "ARKM": "ARKM-USD",
    "ARPA": "ARPA-USD",
    "ARTFI": "ARTFI-USD",
    "ARTY": "ARTY-USD",
    "ARX": "ARX-USD",
    "ASI": "ASI-USD",
    "ASTR": "ASTR-USD",
    "ATA": "ATA-USD",
    "ATH": "ATH-USD",
    "ATOM": "ATOM-USD",
    "ATOM3L": "ATOM3L-USD",
    "ATOM3S": "ATOM3S-USD",
    "AUCTION": "AUCTION-USD",
    "AUDIO": "AUDIO-USD",
    "AURORA": "AURORA-USD",
    "AURY": "AURY-USD",
    "AUTOS": "AUTOS-USD",
    "AVA": "AVA-USD",
    "AVAAI": "AVAAI-USD",
    "AVAIL": "AVAIL-USD",
    "AVAX": "AVAX-USD",
    "AVAX3L": "AVAX3L-USD",
    "AVAX3S": "AVAX3S-USD",
    "AXS": "AXS-USD",
    "AZERO": "AZERO-USD",
    "B3": "B3-USD",
    "BABYBNB": "BABYBNB-USD",
    "BABYDOGE": "BABYDOGE-USD",
    "BABYSHARK": "BABYSHARK-USD",
    "BAL": "BAL-USD",
    "BAN": "BAN-USD",
    "BANANA": "BANANA-USD",
    "BAND": "BAND-USD",
    "BAT": "BAT-USD",
    "BAX": "BAX-USD",
    "BB": "BB-USD",
    "BCH": "BCH-USD",
    "BCH3L": "BCH3L-USD",
    "BCH3S": "BCH3S-USD",
    "BCHSV": "BCHSV-USD",
    "BCUT": "BCUT-USD",
    "BDX": "BDX-USD",
    "BEAT": "BEAT-USD",
    "BEER": "BEER-USD",
    "BEFI": "BEFI-USD",
    "BEPRO": "BEPRO-USD",
    "BERA": "BERA-USD",
    "BFC": "BFC-USD",
    "BICO": "BICO-USD",
    "BIDP": "BIDP-USD",
    "BIFI": "BIFI-USD",
    "BIGTIME": "BIGTIME-USD",
    "BIO": "BIO-USD",
    "BLAST": "BLAST-USD",
    "BLOCK": "BLOCK-USD",
    "BLOK": "BLOK-USD",
    "BLUE": "BLUE-USD",
    "BLUR": "BLUR-USD",
    "BLZ": "BLZ-USD",
    "BMT": "BMT-USD",
    "BMX": "BMX-USD",
    "BN": "BN-USD",
    "BNB": "BNB-USD",
    "BNB3L": "BNB3L-USD",
    "BNB3S": "BNB3S-USD",
    "BNC": "BNC-USD",
    "BOBA": "BOBA-USD",
    "BOBMEME": "BOBMEME-USD",
    "BOME": "BOME-USD",
    "BONDLY": "BONDLY-USD",
    "BONK": "BONK-USD",
    "BOSON": "BOSON-USD",
    "BR": "BR-USD",
    "BRAWL": "BRAWL-USD",
    "BRETT": "BRETT-USD",
    "BRISE": "BRISE-USD",
    "BRL": "BRL-USD",
    "BROCCOLI": "BROCCOLI-USD",
    "BRWL": "BRWL-USD",
    "BSW": "BSW-USD",
    "BTC": "BTC-USD",
    "BTC3L": "BTC3L-USD",
    "BTC3S": "BTC3S-USD",
    "BTCDOWN": "BTCDOWN-USD",
    "BTCUP": "BTCUP-USD",
    "BTF": "BTF-USD",
    "BTT": "BTT-USD",
    "BUBB": "BUBB-USD",
    "BULL": "BULL-USD",
    "BURGER": "BURGER-USD",
    "BUZZ": "BUZZ-USD",
    "C98": "C98-USD",
    "CAKE": "CAKE-USD",
    "CARV": "CARV-USD",
    "CAS": "CAS-USD",
    "CAT": "CAT-USD",
    "CATI": "CATI-USD",
    "CATS": "CATS-USD",
    "CCD": "CCD-USD",
    "CEEK": "CEEK-USD",
    "CELO": "CELO-USD",
    "CELR": "CELR-USD",
    "CERE": "CERE-USD",
    "CETUS": "CETUS-USD",
    "CFG": "CFG-USD",
    "CFX": "CFX-USD",
    "CGPT": "CGPT-USD",
    "CHEEMS": "CHEEMS-USD",
    "CHEQ": "CHEQ-USD",
    "CHILLGUY": "CHILLGUY-USD",
    "CHIRP": "CHIRP-USD",
    "CHMB": "CHMB-USD",
    "CHO": "CHO-USD",
    "CHR": "CHR-USD",
    "CHZ": "CHZ-USD",
    "CIRUS": "CIRUS-USD",
    "CKB": "CKB-USD",
    "CLAY": "CLAY-USD",
    "CLH": "CLH-USD",
    "CLOUD": "CLOUD-USD",
    "CLV": "CLV-USD",
    "COMBO": "COMBO-USD",
    "COMP": "COMP-USD",
    "COOKIE": "COOKIE-USD",
    "COQ": "COQ-USD",
    "COTI": "COTI-USD",
    "COW": "COW-USD",
    "CPOOL": "CPOOL-USD",
    "CREAM": "CREAM-USD",
    "CREDI": "CREDI-USD",
    "CRO": "CRO-USD",
    "CROS": "CROS-USD",
    "CRV": "CRV-USD",
    "CSIX": "CSIX-USD",
    "CSPR": "CSPR-USD",
    "CTA": "CTA-USD",
    "CTC": "CTC-USD",
    "CTI": "CTI-USD",
    "CTRL": "CTRL-USD",
    "CTSI": "CTSI-USD",
    "CVC": "CVC-USD",
    "CVX": "CVX-USD",
    "CWEB": "CWEB-USD",
    "CWS": "CWS-USD",
    "CXT": "CXT-USD",
    "CYBER": "CYBER-USD",
    "D": "D-USD",
    "DAG": "DAG-USD",
    "DAI": "DAI-USD",
    "DAO": "DAO-USD",
    "DAPP": "DAPP-USD",
    "DAPPX": "DAPPX-USD",
    "DASH": "DASH-USD",
    "DATA": "DATA-USD",
    "DBR": "DBR-USD",
    "DC": "DC-USD",
    "DCK": "DCK-USD",
    "DCR": "DCR-USD",
    "DECHAT": "DECHAT-USD",
    "DEEP": "DEEP-USD",
    "DEFI": "DEFI-USD",
    "DEGEN": "DEGEN-USD",
    "DEGO": "DEGO-USD",
    "DENT": "DENT-USD",
    "DEXE": "DEXE-USD",
    "DFI": "DFI-USD",
    "DFYN": "DFYN-USD",
    "DGB": "DGB-USD",
    "DIA": "DIA-USD",
    "DIGIMON": "DIGIMON-USD",
    "DIN": "DIN-USD",
    "DMAIL": "DMAIL-USD",
    "DMTR": "DMTR-USD",
    "DOAI": "DOAI-USD",
    "DODO": "DODO-USD",
    "DOGE": "DOGE-USD",
    "DOGE3L": "DOGE3L-USD",
    "DOGE3S": "DOGE3S-USD",
    "DOGEGOV": "DOGEGOV-USD",
    "DOGS": "DOGS-USD",
    "DOMIN": "DOMIN-USD",
    "DOP": "DOP-USD",
    "DOT": "DOT-USD",
    "DOT3L": "DOT3L-USD",
    "DOT3S": "DOT3S-USD",
    "DPR": "DPR-USD",
    "DREAMS": "DREAMS-USD",
    "DRIFT": "DRIFT-USD",
    "DUCK": "DUCK-USD",
    "DUSK": "DUSK-USD",
    "DVPN": "DVPN-USD",
    "DYDX": "DYDX-USD",
    "DYM": "DYM-USD",
    "DYP": "DYP-USD",
    "E4C": "E4C-USD",
    "EDU": "EDU-USD",
    "EGLD": "EGLD-USD",
    "EGO": "EGO-USD",
    "EGP": "EGP-USD",
    "EIGEN": "EIGEN-USD",
    "ELA": "ELA-USD",
    "ELF": "ELF-USD",
    "ELON": "ELON-USD",
    "EMYC": "EMYC-USD",
    "ENA": "ENA-USD",
    "ENJ": "ENJ-USD",
    "ENS": "ENS-USD",
    "EOS": "EOS-USD",
    "EPIC": "EPIC-USD",
    "EPIK": "EPIK-USD",
    "EPX": "EPX-USD",
    "EQX": "EQX-USD",
    "ERG": "ERG-USD",
    "ERTHA": "ERTHA-USD",
    "ESE": "ESE-USD",
    "ETC": "ETC-USD",
    "ETH": "ETH-USD",
    "ETH2": "ETH2-USD",
    "ETH3L": "ETH3L-USD",
    "ETH3S": "ETH3S-USD",
    "ETHDOWN": "ETHDOWN-USD",
    "ETHFI": "ETHFI-USD",
    "ETHUP": "ETHUP-USD",
    "ETHW": "ETHW-USD",
    "ETN": "ETN-USD",
    "EUL": "EUL-USD",
    "EUR": "EUR-USD",
    "EVER": "EVER-USD",
    "EWT": "EWT-USD",
    "EYWA": "EYWA-USD",
    "F": "F-USD",
    "FARTCOIN": "FARTCOIN-USD",
    "FB": "FB-USD",
    "FCON": "FCON-USD",
    "FEAR": "FEAR-USD",
    "FET": "FET-USD",
    "FIDA": "FIDA-USD",
    "FIL": "FIL-USD",
    "FINC": "FINC-USD",
    "FIRE": "FIRE-USD",
    "FITFI": "FITFI-USD",
    "FLAME": "FLAME-USD",
    "FLIP": "FLIP-USD",
    "FLOKI": "FLOKI-USD",
    "FLOW": "FLOW-USD",
    "FLR": "FLR-USD",
    "FLUX": "FLUX-USD",
    "FOMO": "FOMO-USD",
    "FORM": "FORM-USD",
    "FORT": "FORT-USD",
    "FORTH": "FORTH-USD",
    "FORWARD": "FORWARD-USD",
    "FOXY": "FOXY-USD",
    "FRED": "FRED-USD",
    "FRM": "FRM-USD",
    "FT": "FT-USD",
    "FTON": "FTON-USD",
    "FTT": "FTT-USD",
    "FUEL": "FUEL-USD",
    "FURY": "FURY-USD",
    "FWOG": "FWOG-USD",
    "FX": "FX-USD",
    "FXS": "FXS-USD",
    "G": "G-USD",
    "G3": "G3-USD",
    "G7": "G7-USD",
    "GAFI": "GAFI-USD",
    "GALAX": "GALAX-USD",
    "GALAX3L": "GALAX3L-USD",
    "GALAX3S": "GALAX3S-USD",
    "GAMEAI": "GAMEAI-USD",
    "GARI": "GARI-USD",
    "GAS": "GAS-USD",
    "GEEQ": "GEEQ-USD",
    "GHX": "GHX-USD",
    "GIGA": "GIGA-USD",
    "GLM": "GLM-USD",
    "GLMR": "GLMR-USD",
    "GLQ": "GLQ-USD",
    "GLS": "GLS-USD",
    "GMEE": "GMEE-USD",
    "GMM": "GMM-USD",
    "GMRX": "GMRX-USD",
    "GMT": "GMT-USD",
    "GMX": "GMX-USD",
    "GNS": "GNS-USD",
    "GOAL": "GOAL-USD",
    "GOAT": "GOAT-USD",
    "GOATS": "GOATS-USD",
    "GODL": "GODL-USD",
    "GODS": "GODS-USD",
    "GPS": "GPS-USD",
    "GRAIL": "GRAIL-USD",
    "GRASS": "GRASS-USD",
    "GRIFFAIN": "GRIFFAIN-USD",
    "GRIFT": "GRIFT-USD",
    "GRT": "GRT-USD",
    "GST": "GST-USD",
    "GTAI": "GTAI-USD",
    "GTC": "GTC-USD",
    "GUN": "GUN-USD",
    "GX": "GX-USD",
    "HAI": "HAI-USD",
    "HALO": "HALO-USD",
    "HAPI": "HAPI-USD",
    "HAPPY": "HAPPY-USD",
    "HARD": "HARD-USD",
    "HBAR": "HBAR-USD",
    "HEART": "HEART-USD",
    "HEI": "HEI-USD",
    "HFT": "HFT-USD",
    "HIFI": "HIFI-USD",
    "HIGH": "HIGH-USD",
    "HIP": "HIP-USD",
    "HIPPO": "HIPPO-USD",
    "HLG": "HLG-USD",
    "HLO": "HLO-USD",
    "HMND": "HMND-USD",
    "HMSTR": "HMSTR-USD",
    "HNT": "HNT-USD",
    "HOLD": "HOLD-USD",
    "HOLDCOIN": "HOLDCOIN-USD",
    "HONEY": "HONEY-USD",
    "HOTCROSS": "HOTCROSS-USD",
    "HPOS10I": "HPOS10I-USD",
    "HQ": "HQ-USD",
    "HSK": "HSK-USD",
    "HTR": "HTR-USD",
    "HTX": "HTX-USD",
    "HYDRA": "HYDRA-USD",
    "HYPE": "HYPE-USD",
    "HYVE": "HYVE-USD",
    "ICE": "ICE-USD",
    "ICP": "ICP-USD",
    "ICX": "ICX-USD",
    "ID": "ID-USD",
    "ID3L": "ID3L-USD",
    "ID3S": "ID3S-USD",
    "IDEA": "IDEA-USD",
    "IGU": "IGU-USD",
    "ILV": "ILV-USD",
    "IMT": "IMT-USD",
    "IMX": "IMX-USD",
    "INJ": "INJ-USD",
    "INJDOWN": "INJDOWN-USD",
    "INJUP": "INJUP-USD",
    "INSP": "INSP-USD",
    "IO": "IO-USD",
    "IOST": "IOST-USD",
    "IOTA": "IOTA-USD",
    "IOTX": "IOTX-USD",
    "IP": "IP-USD",
    "IRL": "IRL-USD",
    "ISLAND": "ISLAND-USD",
    "ISLM": "ISLM-USD",
    "ISME": "ISME-USD",
    "ISP": "ISP-USD",
    "ISSP": "ISSP-USD",
    "ITHACA": "ITHACA-USD",
    "IZI": "IZI-USD",
    "J": "J-USD",
    "JAILSTOOL": "JAILSTOOL-USD",
    "JAM": "JAM-USD",
    "JASMY": "JASMY-USD",
    "JASMY3L": "JASMY3L-USD",
    "JASMY3S": "JASMY3S-USD",
    "JELLYJELLY": "JELLYJELLY-USD",
    "JST": "JST-USD",
    "JTO": "JTO-USD",
    "JUP": "JUP-USD",
    "KACE": "KACE-USD",
    "KAGI": "KAGI-USD",
    "KAIA": "KAIA-USD",
    "KAITO": "KAITO-USD",
    "KALT": "KALT-USD",
    "KARATE": "KARATE-USD",
    "KARRAT": "KARRAT-USD",
    "KAS": "KAS-USD",
    "KASDOWN": "KASDOWN-USD",
    "KASUP": "KASUP-USD",
    "KAVA": "KAVA-USD",
    "KCS": "KCS-USD",
    "KDA": "KDA-USD",
    "KEY": "KEY-USD",
    "KILO": "KILO-USD",
    "KIMA": "KIMA-USD",
    "KIP": "KIP-USD",
    "KLV": "KLV-USD",
    "KMD": "KMD-USD",
    "KMNO": "KMNO-USD",
    "KNC": "KNC-USD",
    "KOMA": "KOMA-USD",
    "KOS": "KOS-USD",
    "KPOL": "KPOL-USD",
    "KRL": "KRL-USD",
    "KSM": "KSM-USD",
    "L3": "L3-USD",
    "LADYS": "LADYS-USD",
    "LAI": "LAI-USD",
    "LAVA": "LAVA-USD",
    "LAY3R": "LAY3R-USD",
    "LAYER": "LAYER-USD",
    "LBR": "LBR-USD",
    "LDO": "LDO-USD",
    "LENDS": "LENDS-USD",
    "LFT": "LFT-USD",
    "LIKE": "LIKE-USD",
    "LINA": "LINA-USD",
    "LINGO": "LINGO-USD",
    "LINK": "LINK-USD",
    "LINK3L": "LINK3L-USD",
    "LINK3S": "LINK3S-USD",
    "LISTA": "LISTA-USD",
    "LITH": "LITH-USD",
    "LKI": "LKI-USD",
    "LL": "LL-USD",
    "LLM": "LLM-USD",
    "LMWR": "LMWR-USD",
    "LOCUS": "LOCUS-USD",
    "LOFI": "LOFI-USD",
    "LOGX": "LOGX-USD",
    "LOKA": "LOKA-USD",
    "LOOKS": "LOOKS-USD",
    "LOOM": "LOOM-USD",
    "LPOOL": "LPOOL-USD",
    "LPT": "LPT-USD",
    "LQTY": "LQTY-USD",
    "LRC": "LRC-USD",
    "LRDS": "LRDS-USD",
    "LSD": "LSD-USD",
    "LSK": "LSK-USD",
    "LSS": "LSS-USD",
    "LTC": "LTC-USD",
    "LTC3L": "LTC3L-USD",
    "LTC3S": "LTC3S-USD",
    "LTO": "LTO-USD",
    "LUCE": "LUCE-USD",
    "LUMIA": "LUMIA-USD",
    "LUNA": "LUNA-USD",
    "LUNC": "LUNC-USD",
    "LUNCDOWN": "LUNCDOWN-USD",
    "LUNCUP": "LUNCUP-USD",
    "LVVA": "LVVA-USD",
    "LYX": "LYX-USD",
    "M3M3": "M3M3-USD",
    "MAGIC": "MAGIC-USD",
    "MAHA": "MAHA-USD",
    "MAJOR": "MAJOR-USD",
    "MAK": "MAK-USD",
    "MAN": "MAN-USD",
    "MANA": "MANA-USD",
    "MANEKI": "MANEKI-USD",
    "MANTA": "MANTA-USD",
    "MAPO": "MAPO-USD",
    "MARS4": "MARS4-USD",
    "MARSH": "MARSH-USD",
    "MASA": "MASA-USD",
    "MASK": "MASK-USD",
    "MAV": "MAV-USD",
    "MAVIA": "MAVIA-USD",
    "MAX": "MAX-USD",
    "MBL": "MBL-USD",
    "ME": "ME-USD",
    "MELANIA": "MELANIA-USD",
    "MELOS": "MELOS-USD",
    "MEME": "MEME-USD",
    "MEMEFI": "MEMEFI-USD",
    "MEMHASH": "MEMHASH-USD",
    "MERL": "MERL-USD",
    "METIS": "METIS-USD",
    "MEW": "MEW-USD",
    "MGT": "MGT-USD",
    "MICHI": "MICHI-USD",
    "MIGGLES": "MIGGLES-USD",
    "MILADYCULT": "MILADYCULT-USD",
    "MINA": "MINA-USD",
    "MIND": "MIND-USD",
    "MINT": "MINT-USD",
    "MJT": "MJT-USD",
    "MKR": "MKR-USD",
    "MLK": "MLK-USD",
    "MNDE": "MNDE-USD",
    "MNRY": "MNRY-USD",
    "MNT": "MNT-USD",
    "MOBILE": "MOBILE-USD",
    "MOCA": "MOCA-USD",
    "MOG": "MOG-USD",
    "MON": "MON-USD",
    "MONI": "MONI-USD",
    "MONKY": "MONKY-USD",
    "MOODENG": "MOODENG-USD",
    "MORPHO": "MORPHO-USD",
    "MOVE": "MOVE-USD",
    "MOVR": "MOVR-USD",
    "MOXIE": "MOXIE-USD",
    "MOZ": "MOZ-USD",
    "MPC": "MPC-USD",
    "MPLX": "MPLX-USD",
    "MTL": "MTL-USD",
    "MTOS": "MTOS-USD",
    "MTRG": "MTRG-USD",
    "MTS": "MTS-USD",
    "MTV": "MTV-USD",
    "MUBARAK": "MUBARAK-USD",
    "MUBI": "MUBI-USD",
    "MV": "MV-USD",
    "MXC": "MXC-USD",
    "MXM": "MXM-USD",
    "MYRIA": "MYRIA-USD",
    "MYRO": "MYRO-USD",
    "NAKA": "NAKA-USD",
    "NATIX": "NATIX-USD",
    "NAVI": "NAVI-USD",
    "NAVX": "NAVX-USD",
    "NAYM": "NAYM-USD",
    "NC": "NC-USD",
    "NEAR": "NEAR-USD",
    "NEAR3L": "NEAR3L-USD",
    "NEAR3S": "NEAR3S-USD",
    "NEIRO": "NEIRO-USD",
    "NEIROCTO": "NEIROCTO-USD",
    "NEO": "NEO-USD",
    "NEON": "NEON-USD",
    "NETVR": "NETVR-USD",
    "NFP": "NFP-USD",
    "NFT": "NFT-USD",
    "NGC": "NGC-USD",
    "NGL": "NGL-USD",
    "NIBI": "NIBI-USD",
    "NIL": "NIL-USD",
    "NIM": "NIM-USD",
    "NKN": "NKN-USD",
    "NLK": "NLK-USD",
    "NMR": "NMR-USD",
    "NOOB": "NOOB-USD",
    "NOT": "NOT-USD",
    "NOTAI": "NOTAI-USD",
    "NPC": "NPC-USD",
    "NRN": "NRN-USD",
    "NS": "NS-USD",
    "NTRN": "NTRN-USD",
    "NUM": "NUM-USD",
    "NVG8": "NVG8-USD",
    "NWC": "NWC-USD",
    "NXRA": "NXRA-USD",
    "NYM": "NYM-USD",
    "OAS": "OAS-USD",
    "OBI": "OBI-USD",
    "OBT": "OBT-USD",
    "ODDZ": "ODDZ-USD",
    "OFN": "OFN-USD",
    "OGN": "OGN-USD",
    "OLE": "OLE-USD",
    "OM": "OM-USD",
    "OMG": "OMG-USD",
    "OMNI": "OMNI-USD",
    "OMNIA": "OMNIA-USD",
    "ONDO": "ONDO-USD",
    "ONE": "ONE-USD",
    "ONT": "ONT-USD",
    "OOE": "OOE-USD",
    "OORT": "OORT-USD",
    "OP": "OP-USD",
    "OPAI": "OPAI-USD",
    "OPUL": "OPUL-USD",
    "ORAI": "ORAI-USD",
    "ORBS": "ORBS-USD",
    "ORCA": "ORCA-USD",
    "ORDER": "ORDER-USD",
    "ORDI": "ORDI-USD",
    "ORDIDOWN": "ORDIDOWN-USD",
    "ORDIUP": "ORDIUP-USD",
    "OSMO": "OSMO-USD",
    "OTK": "OTK-USD",
    "OVR": "OVR-USD",
    "OXT": "OXT-USD",
    "PAAL": "PAAL-USD",
    "PAIN": "PAIN-USD",
    "PANDORA": "PANDORA-USD",
    "PARTI": "PARTI-USD",
    "PATEX": "PATEX-USD",
    "PAXG": "PAXG-USD",
    "PBUX": "PBUX-USD",
    "PBX": "PBX-USD",
    "PEAQ": "PEAQ-USD",
    "PEN": "PEN-USD",
    "PENDLE": "PENDLE-USD",
    "PENGU": "PENGU-USD",
    "PEOPLE": "PEOPLE-USD",
    "PEPE": "PEPE-USD",
    "PEPE2": "PEPE2-USD",
    "PEPEDOWN": "PEPEDOWN-USD",
    "PEPEUP": "PEPEUP-USD",
    "PERP": "PERP-USD",
    "PGC": "PGC-USD",
    "PHA": "PHA-USD",
    "PHIL": "PHIL-USD",
    "PIP": "PIP-USD",
    "PIX": "PIX-USD",
    "PIXEL": "PIXEL-USD",
    "PLU": "PLU-USD",
    "PLUME": "PLUME-USD",
    "PMG": "PMG-USD",
    "PNDR": "PNDR-USD",
    "PNUT": "PNUT-USD",
    "POKT": "POKT-USD",
    "POL": "POL-USD",
    "POLC": "POLC-USD",
    "POLK": "POLK-USD",
    "POLS": "POLS-USD",
    "POLYX": "POLYX-USD",
    "PONCH": "PONCH-USD",
    "POND": "POND-USD",
    "PONKE": "PONKE-USD",
    "POPCAT": "POPCAT-USD",
    "PORTAL": "PORTAL-USD",
    "POWER": "POWER-USD",
    "PRCL": "PRCL-USD",
    "PRE": "PRE-USD",
    "PROM": "PROM-USD",
    "PSTAKE": "PSTAKE-USD",
    "PUFFER": "PUFFER-USD",
    "PUMLX": "PUMLX-USD",
    "PUNDIX": "PUNDIX-USD",
    "PURR": "PURR-USD",
    "PUSH": "PUSH-USD",
    "PYR": "PYR-USD",
    "PYTH": "PYTH-USD",
    "PYTHDOWN": "PYTHDOWN-USD",
    "PYTHUP": "PYTHUP-USD",
    "PYUSD": "PYUSD-USD",
    "PZP": "PZP-USD",
    "QI": "QI-USD",
    "QKC": "QKC-USD",
    "QNT": "QNT-USD",
    "QORPO": "QORPO-USD",
    "QTUM": "QTUM-USD",
    "QUICK": "QUICK-USD",
    "QUILL": "QUILL-USD",
    "RACA": "RACA-USD",
    "RATS": "RATS-USD",
    "RAY": "RAY-USD",
    "RBTC1": "RBTC1-USD",
    "RDNT": "RDNT-USD",
    "REACT": "REACT-USD",
    "READY": "READY-USD",
    "REDO": "REDO-USD",
    "REDSTONE": "REDSTONE-USD",
    "REEF": "REEF-USD",
    "REKT": "REKT-USD",
    "REN": "REN-USD",
    "RENDER": "RENDER-USD",
    "REQ": "REQ-USD",
    "REVU": "REVU-USD",
    "REVV": "REVV-USD",
    "REZ": "REZ-USD",
    "RIFSOL": "RIFSOL-USD",
    "RIO": "RIO-USD",
    "RIZ": "RIZ-USD",
    "RLC": "RLC-USD",
    "RMV": "RMV-USD",
    "ROAM": "ROAM-USD",
    "RONIN": "RONIN-USD",
    "ROOBEE": "ROOBEE-USD",
    "ROOT": "ROOT-USD",
    "ROSE": "ROSE-USD",
    "ROUTE": "ROUTE-USD",
    "RPK": "RPK-USD",
    "RPL": "RPL-USD",
    "RSR": "RSR-USD",
    "RUNE": "RUNE-USD",
    "RVN": "RVN-USD",
    "RWA": "RWA-USD",
    "S": "S-USD",
    "SAFE": "SAFE-USD",
    "SAMO": "SAMO-USD",
    "SAND": "SAND-USD",
    "SAROS": "SAROS-USD",
    "SATS": "SATS-USD",
    "SCA": "SCA-USD",
    "SCPT": "SCPT-USD",
    "SCR": "SCR-USD",
    "SCRT": "SCRT-USD",
    "SD": "SD-USD",
    "SDM": "SDM-USD",
    "SEAM": "SEAM-USD",
    "SEED": "SEED-USD",
    "SEI": "SEI-USD",
    "SEIDOWN": "SEIDOWN-USD",
    "SEIUP": "SEIUP-USD",
    "SENSO": "SENSO-USD",
    "SERAPH": "SERAPH-USD",
    "SFI": "SFI-USD",
    "SFP": "SFP-USD",
    "SFUND": "SFUND-USD",
    "SHELL": "SHELL-USD",
    "SHIB": "SHIB-USD",
    "SHIB2L": "SHIB2L-USD",
    "SHIB2S": "SHIB2S-USD",
    "SHR": "SHR-USD",
    "SHRAP": "SHRAP-USD",
    "SIDUS": "SIDUS-USD",
    "SILLY": "SILLY-USD",
    "SIN": "SIN-USD",
    "SIREN": "SIREN-USD",
    "SKEY": "SKEY-USD",
    "SKL": "SKL-USD",
    "SKY": "SKY-USD",
    "SLC": "SLC-USD",
    "SLERF": "SLERF-USD",
    "SLF": "SLF-USD",
    "SLIM": "SLIM-USD",
    "SLING": "SLING-USD",
    "SLN": "SLN-USD",
    "SLP": "SLP-USD",
    "SMH": "SMH-USD",
    "SMILE": "SMILE-USD",
    "SMOLE": "SMOLE-USD",
    "SNAI": "SNAI-USD",
    "SNS": "SNS-USD",
    "SNX": "SNX-USD",
    "SOCIAL": "SOCIAL-USD",
    "SOL": "SOL-USD",
    "SOL3L": "SOL3L-USD",
    "SOL3S": "SOL3S-USD",
    "SOLAYER": "SOLAYER-USD",
    "SOLV": "SOLV-USD",
    "SONIC": "SONIC-USD",
    "SOUL": "SOUL-USD",
    "SPA": "SPA-USD",
    "SPOT": "SPOT-USD",
    "SPX": "SPX-USD",
    "SQD": "SQD-USD",
    "SQR": "SQR-USD",
    "SSV": "SSV-USD",
    "STAGE": "STAGE-USD",
    "STAMP": "STAMP-USD",
    "STG": "STG-USD",
    "STND": "STND-USD",
    "STNK": "STNK-USD",
    "STORE": "STORE-USD",
    "STORJ": "STORJ-USD",
    "STRAX": "STRAX-USD",
    "STREAM": "STREAM-USD",
    "STRK": "STRK-USD",
    "STX": "STX-USD",
    "SUI": "SUI-USD",
    "SUI3L": "SUI3L-USD",
    "SUI3S": "SUI3S-USD",
    "SUIA": "SUIA-USD",
    "SUIP": "SUIP-USD",
    "SUKU": "SUKU-USD",
    "SUN": "SUN-USD",
    "SUNDOG": "SUNDOG-USD",
    "SUPER": "SUPER-USD",
    "SUPRA": "SUPRA-USD",
    "SUSHI": "SUSHI-USD",
    "SUSHI3L": "SUSHI3L-USD",
    "SUSHI3S": "SUSHI3S-USD",
    "SWARMS": "SWARMS-USD",
    "SWASH": "SWASH-USD",
    "SWEAT": "SWEAT-USD",
    "SWELL": "SWELL-USD",
    "SWFTC": "SWFTC-USD",
    "SXP": "SXP-USD",
    "SYLO": "SYLO-USD",
    "SYN": "SYN-USD",
    "SYNT": "SYNT-USD",
    "SYNTH": "SYNTH-USD",
    "SYRUP": "SYRUP-USD",
    "SYS": "SYS-USD",
    "T": "T-USD",
    "TADA": "TADA-USD",
    "TAIKO": "TAIKO-USD",
    "TAO": "TAO-USD",
    "TAOCAT": "TAOCAT-USD",
    "TAP": "TAP-USD",
    "TARA": "TARA-USD",
    "TEL": "TEL-USD",
    "TENET": "TENET-USD",
    "TEVA": "TEVA-USD",
    "TFUEL": "TFUEL-USD",
    "THETA": "THETA-USD",
    "TIA": "TIA-USD",
    "TIADOWN": "TIADOWN-USD",
    "TIAUP": "TIAUP-USD",
    "TIDAL": "TIDAL-USD",
    "TIME": "TIME-USD",
    "TLM": "TLM-USD",
    "TLOS": "TLOS-USD",
    "TNSR": "TNSR-USD",
    "TOKEN": "TOKEN-USD",
    "TOKO": "TOKO-USD",
    "TOMI": "TOMI-USD",
    "TON": "TON-USD",
    "TOSHI": "TOSHI-USD",
    "TOWER": "TOWER-USD",
    "TRAC": "TRAC-USD",
    "TRADE": "TRADE-USD",
    "TRB": "TRB-USD",
    "TRBDOWN": "TRBDOWN-USD",
    "TRBUP": "TRBUP-USD",
    "TREAT": "TREAT-USD",
    "TRISIG": "TRISIG-USD",
    "TRU": "TRU-USD",
    "TRUF": "TRUF-USD",
    "TRUMP": "TRUMP-USD",
    "TRVL": "TRVL-USD",
    "TRX": "TRX-USD",
    "TST": "TST-USD",
    "TSTBSC": "TSTBSC-USD",
    "TSUGT": "TSUGT-USD",
    "TT": "TT-USD",
    "TURBO": "TURBO-USD",
    "TURBOS": "TURBOS-USD",
    "TURT": "TURT-USD",
    "TUSD": "TUSD-USD",
    "TUT": "TUT-USD",
    "TWT": "TWT-USD",
    "U2U": "U2U-USD",
    "UFO": "UFO-USD",
    "ULTI": "ULTI-USD",
    "UMA": "UMA-USD",
    "UNA": "UNA-USD",
    "UNI": "UNI-USD",
    "UNI3L": "UNI3L-USD",
    "UNI3S": "UNI3S-USD",
    "UNIO": "UNIO-USD",
    "UNO": "UNO-USD",
    "UOS": "UOS-USD",
    "UPO": "UPO-USD",
    "UQC": "UQC-USD",
    "URO": "URO-USD",
    "USDC": "USDC-USD",
    "USDD": "USDD-USD",
    "USDE": "USDE-USD",
    "USDJ": "USDJ-USD",
    "USDP": "USDP-USD",
    "USDT": "USDT-USD",
    "USTC": "USTC-USD",
    "USUAL": "USUAL-USD",
    "UTK": "UTK-USD",
    "UXLINK": "UXLINK-USD",
    "VAI": "VAI-USD",
    "VANA": "VANA-USD",
    "VANRY": "VANRY-USD",
    "VELO": "VELO-USD",
    "VEMP": "VEMP-USD",
    "VENOM": "VENOM-USD",
    "VERSE": "VERSE-USD",
    "VET": "VET-USD",
    "VET3L": "VET3L-USD",
    "VET3S": "VET3S-USD",
    "VIDT": "VIDT-USD",
    "VINE": "VINE-USD",
    "VINU": "VINU-USD",
    "VIRTUAL": "VIRTUAL-USD",
    "VISION": "VISION-USD",
    "VOLT": "VOLT-USD",
    "VOXEL": "VOXEL-USD",
    "VR": "VR-USD",
    "VRA": "VRA-USD",
    "VRADOWN": "VRADOWN-USD",
    "VRAUP": "VRAUP-USD",
    "VRTX": "VRTX-USD",
    "VSYS": "VSYS-USD",
    "VTHO": "VTHO-USD",
    "VVV": "VVV-USD",
    "VXV": "VXV-USD",
    "W": "W-USD",
    "WAL": "WAL-USD",
    "WAN": "WAN-USD",
    "WAT": "WAT-USD",
    "WAV": "WAV-USD",
    "WAVES": "WAVES-USD",
    "WAX": "WAX-USD",
    "WAXL": "WAXL-USD",
    "WBTC": "WBTC-USD",
    "WELL": "WELL-USD",
    "WEMIX": "WEMIX-USD",
    "WEN": "WEN-USD",
    "WIF": "WIF-USD",
    "WILD": "WILD-USD",
    "WIN": "WIN-USD",
    "WLD": "WLD-USD",
    "WLDDOWN": "WLDDOWN-USD",
    "WLDUP": "WLDUP-USD",
    "WLKN": "WLKN-USD",
    "WLTH": "WLTH-USD",
    "WMTX": "WMTX-USD",
    "WOD": "WOD-USD",
    "WOO": "WOO-USD",
    "WOOP": "WOOP-USD",
    "WSDM": "WSDM-USD",
    "X": "X-USD",
    "XAI": "XAI-USD",
    "XAVA": "XAVA-USD",
    "XCAD": "XCAD-USD",
    "XCH": "XCH-USD",
    "XCN": "XCN-USD",
    "XCV": "XCV-USD",
    "XDB": "XDB-USD",
    "XDC": "XDC-USD",
    "XEC": "XEC-USD",
    "XEM": "XEM-USD",
    "XEN": "XEN-USD",
    "XETA": "XETA-USD",
    "XION": "XION-USD",
    "XLM": "XLM-USD",
    "XMR": "XMR-USD",
    "XNL": "XNL-USD",
    "XNO": "XNO-USD",
    "XOXO": "XOXO-USD",
    "XPR": "XPR-USD",
    "XPRT": "XPRT-USD",
    "XR": "XR-USD",
    "XRD": "XRD-USD",
    "XRP": "XRP-USD",
    "XRP3L": "XRP3L-USD",
    "XRP3S": "XRP3S-USD",
    "XTAG": "XTAG-USD",
    "XTER": "XTER-USD",
    "XTM": "XTM-USD",
    "XTZ": "XTZ-USD",
    "XYM": "XYM-USD",
    "XYO": "XYO-USD",
    "XYRO": "XYRO-USD",
    "YFI": "YFI-USD",
    "YGG": "YGG-USD",
    "YULI": "YULI-USD",
    "ZBCN": "ZBCN-USD",
    "ZCX": "ZCX-USD",
    "ZEC": "ZEC-USD",
    "ZEE": "ZEE-USD",
    "ZELIX": "ZELIX-USD",
    "ZEN": "ZEN-USD",
    "ZEND": "ZEND-USD",
    "ZERC": "ZERC-USD",
    "ZEREBRO": "ZEREBRO-USD",
    "ZERO": "ZERO-USD",
    "ZETA": "ZETA-USD",
    "ZEUS": "ZEUS-USD",
    "ZEX": "ZEX-USD",
    "ZIL": "ZIL-USD",
    "ZK": "ZK-USD",
    "ZKF": "ZKF-USD",
    "ZKJ": "ZKJ-USD",
    "ZKL": "ZKL-USD",
    "ZND": "ZND-USD",
    "ZOO": "ZOO-USD",
    "ZPAY": "ZPAY-USD",
    "ZRC": "ZRC-USD",
    "ZRO": "ZRO-USD",
    "ZRX": "ZRX-USD"
}

# Identify and remove duplicate tickers that exist in both lists
CRYPTO = list(CRYPTO_SYMBOLS.keys())
CRYPTO_SET = set(CRYPTO)

# Check for duplicates between SP500 and CRYPTO
DUPLICATE_TICKERS = SP500_SET.intersection(CRYPTO_SET)
if DUPLICATE_TICKERS:
    logger.warning(f"Found duplicate tickers in SP500 and CRYPTO: {DUPLICATE_TICKERS}")

# Load list of supported KuCoin tokens (skipping header row)
with open("kucoinspotokens.txt", "r") as f:
    kucoin_tokens = set(line.strip() for line in f.readlines()[1:])


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

def get_stock_ohlc(symbol, label, retries=3, delay=1):
    # Try Alpaca for 1d timeframe first
    if label == "1d":
        try:
            end = datetime.utcnow()
            start = end - timedelta(days=365)
            bars = client.get_stock_bars(StockBarsRequest(symbol_or_symbols=symbol, start=start, end=end, timeframe=TimeFrame.Day))
            df = bars.df
            if not df.empty:
                df = df[df.index.get_level_values(0) == symbol]
                df = df.sort_index()
                if len(df) >= 6:  # Make sure we have enough data
                    return df[["high", "low", "close"]]
                logger.warning(f"{symbol} ({label}) - Not enough Alpaca data points: {len(df)}")
        except Exception as e:
            logger.warning(f"{symbol} ({label}) - Alpaca error: {e}")
    
    # Try using direct requests to Yahoo Finance API
    try:
        end_timestamp = int(datetime.now().timestamp())
        
        # Adjust lookback period based on timeframe
        if label == "1m":
            start_timestamp = end_timestamp - (10 * 31536000)  # 10 years in seconds
        elif label == "1w":
            start_timestamp = end_timestamp - (5 * 31536000)  # 5 years in seconds
        else:
            start_timestamp = end_timestamp - 31536000  # 1 year in seconds
        
        if label == "1d":
            interval = "1d"
        elif label == "1w":
            interval = "1wk"
        else:
            interval = "1mo"
        
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
        params = {
            "period1": start_timestamp,
            "period2": end_timestamp,
            "interval": interval,
            "includePrePost": False
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            
            if "chart" in data and "result" in data["chart"] and data["chart"]["result"]:
                result = data["chart"]["result"][0]
                
                # Extract timestamp and price data
                if "timestamp" not in result or "indicators" not in result or "quote" not in result["indicators"] or not result["indicators"]["quote"]:
                    logger.warning(f"{symbol} ({label}) - Yahoo API missing required data structure")
                else:
                    timestamps = result["timestamp"]
                    quote = result["indicators"]["quote"][0]
                    
                    # Check for all required keys
                    if not all(key in quote for key in ["high", "low", "close"]):
                        logger.warning(f"{symbol} ({label}) - Yahoo API missing required price data")
                    else:
                        # Create dataframe
                        df = pd.DataFrame({
                            "timestamp": pd.to_datetime(timestamps, unit="s"),
                            "high": quote["high"],
                            "low": quote["low"],
                            "close": quote["close"]
                        })
                        
                        # Clean data
                        df = df.dropna()
                        df.set_index("timestamp", inplace=True)
                        
                        logger.info(f"{symbol} ({label}) - Retrieved {len(df)} data points from Yahoo API")
                        
                        if len(df) >= 6:
                            return df
                        else:
                            logger.warning(f"{symbol} ({label}) - Not enough data points from Yahoo API: {len(df)}")
            else:
                logger.warning(f"{symbol} ({label}) - No results returned from Yahoo API")
        else:
            logger.warning(f"{symbol} ({label}) - Yahoo API HTTP error: {response.status_code}")
    
    except Exception as e:
        logger.warning(f"{symbol} ({label}) - Yahoo API error: {e}")
    
    # Fall back to yfinance as last resort
    for attempt in range(retries):
        try:
            # Increase backoff time with each retry
            backoff_delay = delay * (2 ** attempt)
            
            # Define headers for the request
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            
            # Try a different approach for each attempt, with timeframe-specific periods
            if attempt == 0:
                interval = "1d" if label == "1d" else "1wk" if label == "1w" else "1mo"
                
                if label == "1m":
                    df = yf.download(symbol, period="10y", interval=interval, progress=False, headers=headers)
                elif label == "1w":
                    df = yf.download(symbol, period="5y", interval=interval, progress=False, headers=headers)
                else:
                    df = yf.download(symbol, period="1y", interval=interval, progress=False, headers=headers)
                
            elif attempt == 1:
                interval = "1d" if label == "1d" else "1wk" if label == "1w" else "1mo"
                
                if label == "1m":
                    df = yf.download(symbol, period="max", interval=interval, progress=False, headers=headers)
                elif label == "1w":
                    df = yf.download(symbol, period="10y", interval=interval, progress=False, headers=headers)
                else:
                    df = yf.download(symbol, period="2y", interval=interval, progress=False, headers=headers)
                
            else:
                # Last attempt with explicit date ranges
                end_date = datetime.now()
                
                if label == "1m":
                    start_date = end_date - timedelta(days=365*10)  # 10 years
                elif label == "1w":
                    start_date = end_date - timedelta(days=365*5)   # 5 years
                else:
                    start_date = end_date - timedelta(days=365*2)   # 2 years
                
                interval = "1d" if label == "1d" else "1wk" if label == "1w" else "1mo"
                df = yf.download(
                    symbol, 
                    start=start_date.strftime('%Y-%m-%d'), 
                    end=end_date.strftime('%Y-%m-%d'), 
                    interval=interval, 
                    progress=False,
                    headers=headers
                )
            
            if df.empty or len(df) < 1:
                logger.warning(f"{symbol} ({label}) - YFinance returned empty dataframe (attempt {attempt+1})")
                time.sleep(backoff_delay)
                continue
                
            if not all(col in df.columns for col in ["High", "Low", "Close"]):
                logger.warning(f"{symbol} ({label}) - YFinance missing required columns (attempt {attempt+1})")
                time.sleep(backoff_delay)
                continue
                
            df.index.name = "timestamp"
            df = df[["High", "Low", "Close"]].rename(columns={"High": "high", "Low": "low", "Close": "close"})
            df = df.dropna()
            
            logger.info(f"{symbol} ({label}) - Retrieved {len(df)} data points from YFinance (attempt {attempt+1})")
            
            if len(df) < 6:
                logger.warning(f"{symbol} ({label}) - Not enough YFinance data points: {len(df)}")
                time.sleep(backoff_delay)
                continue
                
            return df
        except Exception as e:
            logger.warning(f"{symbol} ({label}) - YFinance attempt {attempt+1} error: {e}")
            time.sleep(backoff_delay)
    
    logger.warning(f"{symbol} ({label}) - Failed to get data after all attempts")
    return None

def get_kucoin_ohlc(symbol, timeframe="1d", retries=3, delay=3):
    """
    Fetch daily OHLC data from KuCoin
    """
    if timeframe != "1d":
        logger.warning(f"{symbol} - KuCoin API only supports daily candles directly")
        return None  # KuCoin free API doesn't support weekly/monthly natively

    for attempt in range(retries):
        try:
            now = int(time.time())
            one_year_ago = now - 86400 * 365

            candles = kucoin_client.get_kline_data(symbol, '1day', one_year_ago, now)
            if not candles or not isinstance(candles, list):
                logger.warning(f"{symbol} - No candles returned from KuCoin")
                return None

            df = pd.DataFrame(candles, columns=["time", "open", "close", "high", "low", "volume", "turnover"])

            # Convert all numeric fields to float to avoid Supertrend errors
            for col in ["open", "close", "high", "low", "volume", "turnover"]:
                df[col] = pd.to_numeric(df[col], errors='coerce')

            # Fix for FutureWarning: ensure time is numeric
            df["timestamp"] = pd.to_datetime(pd.to_numeric(df["time"]), unit="s")
            df.set_index("timestamp", inplace=True)
            df = df.sort_index()

            return df[["high", "low", "close"]]
        except Exception as e:
            logger.warning(f"{symbol} - KuCoin fetch attempt {attempt+1} failed: {e}")
            time.sleep(delay * (attempt + 1))  # Exponential backoff
    
    return None

def get_kucoin_aggregated_ohlc(symbol, timeframe="1w", retries=3, delay=3):
    """
    Aggregate daily data from KuCoin to weekly or monthly timeframes
    """
    df_daily = get_kucoin_ohlc(symbol, timeframe="1d", retries=retries, delay=delay)
    if df_daily is None or df_daily.empty:
        logger.warning(f"{symbol} ({timeframe}) - No daily data available for aggregation")
        return None

    try:
        if timeframe == "1w":
            rule = "W"  # Weekly aggregation
            logger.info(f"{symbol} - Aggregating daily data to weekly")
        elif timeframe == "1m":
            rule = "M"  # Monthly aggregation
            logger.info(f"{symbol} - Aggregating daily data to monthly")
        else:
            logger.warning(f"{symbol} - Unsupported timeframe for aggregation: {timeframe}")
            return None

        # Aggregate the daily data
        df_agg = pd.DataFrame()
        df_agg["high"] = df_daily["high"].resample(rule).max()
        df_agg["low"] = df_daily["low"].resample(rule).min()
        df_agg["close"] = df_daily["close"].resample(rule).last()
        
        # Remove NaN values
        df_agg.dropna(inplace=True)
        
        # Ensure we have enough data
        if len(df_agg) < 6:
            logger.warning(f"{symbol} ({timeframe}) - Not enough aggregated data points: {len(df_agg)}")
            return None
            
        logger.info(f"{symbol} ({timeframe}) - Successfully aggregated {len(df_agg)} data points")
        return df_agg
    except Exception as e:
        logger.warning(f"{symbol} ({timeframe}) - KuCoin aggregation failed: {e}")
        return None


def calculate_supertrend(df, timeframe):
    try:
        # Use different parameters based on timeframe
        if timeframe == "1m":
            # Monthly parameters
            atr_period = 50
            multiplier = 5.0
        elif timeframe == "1w":
            # Weekly parameters
            atr_period = 21
            multiplier = 4.0
        else:
            # Daily parameters (default)
            atr_period = 10
            multiplier = 3.0
            
        st = ta.supertrend(df['high'], df['low'], df['close'], length=atr_period, multiplier=multiplier)
        if st is None or st.empty:
            return None
        return df.join(st)
    except Exception as e:
        logger.warning(f"Supertrend calculation failed: {e}")
        return None

def detect_flips(df, display_symbol, existing, timeframe):
    # Determine which Supertrend column to use based on timeframe
    if timeframe == "1m":
        supert_col = 'SUPERT_50_5.0'
    elif timeframe == "1w":
        supert_col = 'SUPERT_21_4.0'
    else:
        supert_col = 'SUPERT_10_3.0'
    
    if supert_col not in df.columns:
        logger.warning(f"{display_symbol} missing {supert_col} column. Skipping.")
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
            
        if prev[supert_col] > prev['close'] and curr[supert_col] < curr['close']:
            new_flips.append({"date": date_str, "type": "green"})
        elif prev[supert_col] < prev['close'] and curr[supert_col] > curr['close']:
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

            df = calculate_supertrend(df, label)
            if df is None:
                logger.warning(f"{display_symbol} ({label}) - Supertrend failed.")
                continue

            before = len(flip_data.get(display_symbol, []))
            detect_flips(df, display_symbol, flip_data, label)
            after = len(flip_data.get(display_symbol, []))
            logger.info(f"{display_symbol} ({label}) - {after - before} new flips.")

            if label in ["1w", "1m"]:
                time.sleep(1.5 + random.uniform(0.5, 1.0))
            else:
                time.sleep(0.5)

        save_flip_history(flip_data, filename)
        logger.info(f"✅ STOCKS flip detection complete for {label.upper()} timeframe.")

def run_crypto(timeframes=None):
    if timeframes is None:
        timeframes = ["1d", "1w"]  # Support only daily and weekly timeframes (removed 1m)

    for label in timeframes:
        filename = f"public_flips_crypto_{label}.json"
        flip_data = load_flip_history(filename)

        for display_symbol in CRYPTO:
            if display_symbol in DUPLICATE_TICKERS:
                logger.info(f"🔍 Skipping {display_symbol} as it exists in stock list")
                continue

            logger.info(f"🔍 Processing {display_symbol} ({label})")
            
            if display_symbol in kucoin_tokens:
                logger.info(f"{display_symbol} ({label}) - 🪙 Using KuCoin")
                kucoin_symbol = f"{display_symbol}-USDT"
                
                if label == "1d":
                    df = get_kucoin_ohlc(kucoin_symbol, timeframe=label)
                else:
                    df = get_kucoin_aggregated_ohlc(kucoin_symbol, timeframe=label)
            else:
                logger.warning(f"{display_symbol} ({label}) - ❌ Not available on KuCoin")
                continue

            if df is None or len(df) < 6:
                logger.warning(f"{display_symbol} ({label}) - Not enough data.")
                continue

            df = calculate_supertrend(df, label)
            if df is None:
                logger.warning(f"{display_symbol} ({label}) - Supertrend calculation failed.")
                continue

            before = len(flip_data.get(display_symbol, []))
            detect_flips(df, display_symbol, flip_data, label)
            after = len(flip_data.get(display_symbol, []))
            logger.info(f"{display_symbol} ({label}) - {after - before} new flips.")
            time.sleep(1.5 + random.uniform(0.5, 1.0))

        save_flip_history(flip_data, filename)
        logger.info(f"✅ CRYPTO flip detection complete for {label.upper()} timeframe.")

# 🔀 CLI-controlled entry point
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--stocks", action="store_true", help="Run stock flips only")
    parser.add_argument("--crypto", action="store_true", help="Run crypto flips only")
    parser.add_argument("--timeframe", choices=["1d", "1w"], help="Specific timeframe to run (used with --crypto)")
    args = parser.parse_args()

    if args.stocks:
        logger.info("📈 Running STOCK flip update only")
        run_stocks()

    elif args.crypto:
        logger.info("🪙 Running CRYPTO flip update only")
        if args.timeframe:
            run_crypto(timeframes=[args.timeframe])
        else:
            run_crypto()

    else:
        logger.info("⚙️ Running FULL update (stocks + crypto)")
        run_stocks()
        run_crypto()
