import yfinance as yf
import json

# Load tickers from your public_flips.json file
with open("public_flips.json", "r") as f:
    data = json.load(f)

tickers = list(data.keys())
company_info = {}

for ticker in tickers:
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        name = info.get("shortName") or info.get("longName") or ""
        if name:
            company_info[ticker] = {"name": name}
    except Exception as e:
        print(f"Error fetching info for {ticker}: {e}")

with open("company_info.json", "w") as f:
    json.dump(company_info, f, indent=2)
