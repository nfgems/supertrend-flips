import yfinance as yf
import json
import time

# Load tickers from your public_flips.json file
with open("public_flips.json", "r") as f:
    data = json.load(f)

tickers = list(data.keys())
company_info = {}

def fetch_company_name(ticker, max_retries=5, base_delay=2):
    for attempt in range(1, max_retries + 1):
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            name = info.get("shortName") or info.get("longName") or ""
            if name:
                return name
            else:
                raise ValueError("Name not found")
        except Exception as e:
            print(f"[{ticker}] Attempt {attempt} failed: {e}")
            if attempt == max_retries:
                print(f"[{ticker}] Giving up after {max_retries} attempts.")
                return ""
            sleep_time = base_delay * (2 ** (attempt - 1))  # Exponential backoff
            print(f"[{ticker}] Retrying in {sleep_time:.1f}s...")
            time.sleep(sleep_time)

# Loop through all tickers and fetch names with retries
for ticker in tickers:
    name = fetch_company_name(ticker)
    if name:
        company_info[ticker] = {"name": name}

# Save to company_info.json
with open("company_info.json", "w") as f:
    json.dump(company_info, f, indent=2)

