import json
import time
import os
import requests

API_KEY = os.getenv("FMP_API_KEY")
FMP_BASE_URL = "https://financialmodelingprep.com/api/v3/profile"

# Load tickers from your public_flips.json file
with open("public_flips.json", "r") as f:
    data = json.load(f)

tickers = list(data.keys())
company_info = {}

def fetch_company_name(ticker, base_delay=5, cooldown_threshold=10, cooldown_time=60):
    attempt = 1
    while True:
        try:
            url = f"{FMP_BASE_URL}/{ticker}?apikey={API_KEY}"
            response = requests.get(url)
            response.raise_for_status()
            result = response.json()
            if result and isinstance(result, list) and "companyName" in result[0]:
                return result[0]["companyName"]
            else:
                raise ValueError("Company name not found in API response")
        except Exception as e:
            print(f"[{ticker}] Attempt {attempt} failed: {e}")
            sleep_time = base_delay * (2 ** (attempt - 1))  # Exponential backoff
            print(f"[{ticker}] Retrying in {sleep_time:.1f}s...")
            time.sleep(sleep_time)

            if attempt % cooldown_threshold == 0:
                print(f"[{ticker}] Cooldown: Waiting {cooldown_time}s after {attempt} attempts.")
                time.sleep(cooldown_time)

            attempt += 1

# Loop through all tickers and fetch names with retry logic
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
