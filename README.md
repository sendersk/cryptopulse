# CryptoPulse — Cryptocurrency Analytics Dashboard

CryptoPulse is a modern Flask-based web application that visualizes cryptocurrency market data in real-time.  
It connects to the **CoinGecko API**, fetches live prices of the **top 10 cryptocurrencies**, and presents analytics such as average prices, 24h changes, and trading volumes — all in a clean, dark-themed dashboard.

---

## Features

✅ Fetches live market data from [CoinGecko API](https://www.coingecko.com/en/api)  
✅ Displays top 10 cryptocurrencies (BTC, ETH, SOL, etc.)  
✅ Shows current price, 24h change, and volume  
✅ Calculates average price & 24h change across all coins  
✅ Dark theme interface (TailwindCSS)  
✅ Ready for expansion: historical trends, charts, exports, alerts  

---

## Tech Stack

| Category | Tools / Libraries |
|-----------|------------------|
| **Backend** | Python, Flask |
| **API & Data** | CoinGecko REST API, Requests |
| **Data Analysis** | Pandas, NumPy |
| **Frontend** | HTML, Jinja2, Tailwind CSS |
| **Visualization (next step)** | Chart.js / Plotly.js |
| **Utilities** | Logging, JSON, CSV |

---

## Project Structure

```bash
cryptopulse/
│
├── app.py # Flask app (routes & templates)
├── crypto_api.py # API connection to CoinGecko
├── data_analysis.py # Basic data analytics
├── utils.py # Utility functions (optional)
│
├── templates/
│ ├── index.html # Dashboard view
│ └── analytics.html # Charts & statistics (next steps)
│
├── static/
│ ├── style.css # Tailwind / dark theme
│ └── theme.js # Theme toggling logic
│
├── data/ # Exported CSV/JSON data
│
├── requirements.txt # Dependencies
└── README.md # Documentation
```

---

## Installation & Run

### 1. Clone the repository

git clone https://github.com/sendersk/cryptopulse.git
cd cryptopulse

### 2. Install dependencies

pip install -r requirements.txt

### 3. Run the Flask app

```bash
python app.py
```
Then open your browser at:
http://127.0.0.1:5000

---

# Future Improvements

- Compare multiple coins
- Export data to CSV/JSON
- Add notifications for major price changes

## Author

Created by **Przemysław Senderski**