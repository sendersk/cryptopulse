from pickletools import float8

import requests
import logging
import time
import json
import os
import pandas as pd


# CONFIGURATION
API_BASE_URL = "https://api.coingecko.com/api/v3"
HEADERS = {"Accept": "application/json"}
OUTPUT_DIR = "data"


def fetch_top_coins(vs_currency: str = "usd", limit: int = 10, retries: int = 3, delay: float = 2.0):
    """
    Fetches the top N cryptocurrencies by market capitalization from the CoinGecko API.

    Args:
        vs_currency (str): The currency to convert crypto prices into (e.g. 'usd', 'eur').
        limit (int): Number of cryptocurrencies to fetch (default 10).
        retries (int): Number of retry attempts if the request fails.
        delay (float): Delay between retries in seconds.

    Returns:
        list[dict]: A list of dictionaries containing crypto data (name, symbol, price, change, etc.)
    """
    url = f"{API_BASE_URL}/coins/markets"
    params = {
        "vs_currency": vs_currency,
        "order": "market_cap_desc",
        "per_page": limit,
        "page": 1,
        "sparkline": False,
    }

    for attempt in range(1, retries + 1):
        try:
            logging.info(f"Fetching top {limit} coins (attempt {attempt}/{retries})...")
            response = requests.get(url, headers=HEADERS, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            # Keep only relevant fields
            cleaned_data = [
                {
                    "name": coin.get("name"),
                    "symbol": coin.get("symbol", "").upper(),
                    "current_price": coin.get("current_price", 0),
                    "price_change_percentage_24h": coin.get("price_change_percentage_24h")
                                                   or coin.get("price_change_percentage_24h_in_currency", 0),
                    "total_volume": coin.get("total_volume", 0),
                    "market_cap": coin.get("market_cap", 0),
                    "image": coin.get("image"),
                }
                for coin in data
            ]

            logging.info(f"Successfully fetched {len(cleaned_data)} coins from CoinGecko API.")
            return cleaned_data

        except requests.exceptions.RequestException as e:
            logging.warning(f"API request failed ({attempt}/{retries}): {e}")
            if attempt < retries:
                logging.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                logging.error("Failed to fetch data from CoinGecko after multiple attempts.")
                return []


def save_latest_data(data, filename="latest_cryptos.json"):
    """
    Saves the latest fetched data to a JSON file in the 'data' directory.

    Args:
        data (list[dict]): The crypto data to save.
        filename (str): Name of the output file.
    """
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    logging.info(f"Saved data to {filepath}")


def get_data_as_dataframe(data):
    """
    Converts list of dictionaries to a pandas DataFrame.

    Args:
        data (list[dict]): The fetched crypto data.

    Returns:
        pd.DataFrame: DataFrame for further analysis and visualization.
    """
    if not data:
        return pd.DataFrame()

    df = pd.DataFrame(data)
    df["current_price"] = df["current_price"].astype(float)
    df["price_change_percentage_24h"] = df["price_change_percentage_24h"].astype(float)
    df["market_cap"] = df["market_cap"].astype(float)
    df["total_volume"] = df["total_volume"].astype(float)
    return df


# LOCAL TESTING

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler()]
    )

    print("\n Testing CoinGecko API connection...\n")

    coins = fetch_top_coins()

    if coins:
        # Save raw data for inspection
        save_latest_data(coins)

        #Convert to DataFrame for quick preview
        df = get_data_as_dataframe(coins)
        print("\n Top 10 Cryptocurrencies:\n")
        print(df[["name", "symbol", "current_price", "price_change_percentage_24h"]])
    else:
        print("\n Failed to fetch data from CoinGecko API.\n")