import yfinance as yf
import json
import time

# Load tickers from your public_flips.json file
with open("public_flips.json", "r") as f:
    data = json.load(f)

tickers = list(data.keys())
company_info = {}

def fetch_company_name(ticker, base_delay=5, cooldown_threshold=10, cooldown_time=60):
    attempt = 1
    while True:
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
            sleep_time = base_delay * (2 ** (attempt - 1))  # Exponential backoff
            print(f"[{ticker}] Retrying in {sleep_time:.1f}s...")
            time.sleep(sleep_time)

            if attempt % cooldown_threshold == 0:
                print(f"[{ticker}] Cooldown: Waiting {cooldown_time}s after {attempt} attempts.")
                time.sleep(cooldown_time)

            attempt += 1

# Loop through all tickers and fetch names with robust retry logic
for i, ticker in enumerate(tickers):
    name = fetch_company_name(ticker)
    if name:
        company_info[ticker] = {"name": name}

    if (i + 1) % 10 == 0:
        print(f"[Batch Cooldown] Sleeping 60s after {i+1} tickers...")
        time.sleep(60)

# Save to company_info.json
with open("company_info.json", "w") as f:
    json.dump(company_info, f, indent=2)
