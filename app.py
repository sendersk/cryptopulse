from flask import Flask, render_template, request
import pandas as pd
import logging
from crypto_api import fetch_top_coins
from data_analysis import load_data, compute_summary, top_movers, correlation_matrix
import os

# Initialize Flask app
app = Flask(__name__)

DATA_PATH = os.path.join("data", "latest_cryptos.json")

# ROUTE: Home — show live crypto dashboard
@app.route("/")
def index():
    """Main dashboard: show list of top cryptocurrencies."""

    # If no data yet, fetch new one
    if not os.path.exists(DATA_PATH):
        logging.info("No local data found. Fetching from API...")
        fetch_top_coins()

    # Load data into DataFrame
    df = load_data(DATA_PATH)

    # Optional sorting / filtering
    sort_by = request.args.get("sort")
    order = request.args.get("order", "desc")

    if sort_by in df.columns:
        df = df.sort_values(by=sort_by, ascending=(order == "asc"))

    # Render template
    return render_template(
        "index.html",
        cryptos=df.to_dict(orient="records")
    )


# ROUTE: Analytics
@app.route("/analytics")
def analytics():
    """Display summary stats, top movers and correlation matrix."""

    df = load_data(DATA_PATH)
    if df.empty:
        return "<h2>No data available. Please run the scraper first.</h2>"

    summary = compute_summary(df)
    movers = top_movers(df)
    corr = correlation_matrix(df)

    # Prepare JSON-serializable objects
    chart_data = {
        "names": df["name"].tolist(),
        "prices": df["current_price"].tolist(),
        "changes": df["price_change_percentage_24h"].tolist()
    }

    return render_template(
        "analytics.html",
        summary=summary,
        top_gainers=movers["top_gainers"].to_dict(orient="records"),
        top_losers=movers["top_losers"].to_dict(orient="records"),
        corr=corr.to_html(classes="corr-table"),
        chart_data=chart_data
    )


# ROUTE: Charts
@app.route("/charts")
def charts():
    data = fetch_top_coins()
    if data is None:
        return "Error: could not fetch data from API", 500

    chart_data = {
        "names": [coin["name"] for coin in data],
        "prices": [coin["current_price"] for coin in data],
        "volumes": [coin["total_volume"] for coin in data],
        "changes": [coin["price_change_percentage_24h"] for coin in data],
    }

    return render_template("charts.html", chart_data=chart_data)


# MAIN ENTRY POINT
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler()]
    )

    app.run(debug=True)
