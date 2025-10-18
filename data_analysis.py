import pandas as pd
import json
import os
import logging
from typing import Dict, Any

DATA_DIR = "data"
LATEST_FILE = "latest_cryptos.json"


# LOAD DATA
def load_data(filepath: str = os.path.join(DATA_DIR, LATEST_FILE)) -> pd.DataFrame:
    """
    Loads cryptocurrency data from a JSON file into a pandas DataFrame.

    Args:
        filepath (str): Path to the JSON file.

    Returns:
        pd.DataFrame: DataFrame containing cryptocurrency data.
    """
    if not os.path.exists(filepath):
        logging.error(f"File not found: {filepath}")
        return pd.DataFrame()

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    df = pd.DataFrame(data)

    # Ensure numeric columns are correctly typed
    for col in ["current_price", "price_change_percentage_24h", "market_cap", "total_volume"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    logging.info(f"Loaded {len(df)} cryptocurrencies from {filepath}")
    return df


# ANALYSIS FUNCTIONS
def compute_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Computes key summary statistics for the dataset.

    Args:
        df (pd.DataFrame): The crypto dataset.

    Returns:
        dict: Summary of main statistics.
    """
    if df.empty:
        logging.warning("Empty DataFrame received for summary computation.")
        return {}

    summary = {
        "total_coins": len(df),
        "average_price": round(df["current_price"].mean(), 2),
        "average_change_24h": round(df["price_change_percentage_24h"].mean(), 2),
        "total_market_cap": round(df["market_cap"].sum(), 2),
        "total_volume": round(df["total_volume"].sum(), 2),
    }

    logging.info("Computed dataset summary statistics.")
    return summary


def top_movers(df: pd.DataFrame, n: int = 3) -> Dict[str, pd.DataFrame]:
    """
    Finds the top gainers and losers by 24h percentage change.

    Args:
        df (pd.DataFrame): The crypto dataset.
        n (int): Number of top/bottom entries to return.

    Returns:
        dict: Two DataFrames — top_gainers and top_losers.
    """
    if df.empty:
        return {"top_gainers": pd.DataFrame(), "top_losers": pd.DataFrame()}

    top_gainers = df.nlargest(n, "price_change_percentage_24h")[["name", "symbol", "price_change_percentage_24h"]]
    top_losers = df.nsmallest(n, "price_change_percentage_24h")[["name", "symbol", "price_change_percentage_24h"]]

    logging.info(f"Identified top {n} gainers and losers.")
    return {"top_gainers": top_gainers, "top_losers": top_losers}


def correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates the correlation matrix for numeric columns.

    Args:
        df (pd.DataFrame): The crypto dataset.

    Returns:
        pd.DataFrame: Correlation matrix between numeric variables.
    """
    if df.empty:
        return pd.DataFrame()

    corr = df[["current_price", "price_change_percentage_24h", "market_cap", "total_volume"]].corr()
    logging.info("Computed correlation matrix.")
    return corr


# LOCAL TEST
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler()]
    )

    print("\n Testing Crypto Data Analysis Module...\n")

    df = load_data()

    if df.empty:
        print(" No data found. Run crypto_api.py first to fetch fresh data.")
    else:
        summary = compute_summary(df)
        movers = top_movers(df)
        corr = correlation_matrix(df)

        print("\n Summary:\n", summary)
        print("\n Top Gainers:\n", movers["top_gainers"])
        print("\n Top Losers:\n", movers["top_losers"])
        print("\n Correlation Matrix:\n", corr)
