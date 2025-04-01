import json
import time
import requests
import os

# Get API key from GitHub Secrets or environment
API_KEY = os.getenv("FMP_API_KEY")
FMP_BASE_URL = "https://financialmodelingprep.com/api/v3/profile"

if not API_KEY:
    raise ValueError("FMP_API_KEY not set in environment variables.")

# Load tickers from public_flips.json
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
            if response.status_code == 403:
                print(f"[{ticker}] 403 Rate limit hit. Waiting 25 hours.")
                time.sleep(25 * 60 * 60)
                continue
            response.raise_for_status()
            result = response.json()
            if result and isinstance(result, list) and "companyName" in result[0]:
                return result[0]["companyName"]
            else:
                raise ValueError("Company name not found in API response")
        except Exception as e:
            print(f"[{ticker}] Attempt {attempt} failed: {e}")
            sleep_time = base_delay * (2 ** (attempt - 1))
            print(f"[{ticker}] Retrying in {sleep_time:.1f}s...")
            time.sleep(sleep_time)

            if attempt % cooldown_threshold == 0:
                print(f"[{ticker}] Cooldown: Waiting {cooldown_time}s after {attempt} attempts.")
                time.sleep(cooldown_time)

            attempt += 1

# Main loop
for i, ticker in enumerate(tickers):
    name = fetch_company_name(ticker)
    if name:
        company_info[ticker] = {"name": name}

    if (i + 1) % 10 == 0:
        print(f"[Batch Cooldown] Sleeping 60s after {i+1} tickers...")
        time.sleep(60)

# Save results
with open("company_info.json", "w") as f:
    json.dump(company_info, f, indent=2)
