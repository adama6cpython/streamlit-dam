import streamlit as st
import yfinance as yf
import datetime
import plotly.graph_objs as go
from bs4 import BeautifulSoup
import requests

# Set up the page configuration and title
st.set_page_config(layout="wide", page_title="Market Overview and Stock Analysis")

# Sidebar for stock selection and date range
st.sidebar.title("Input Ticker")
symbol = st.sidebar.text_input('Enter stock symbol (e.g., NVDA, AAPL):', 'NVDA').upper()
sdate = st.sidebar.date_input('Start Date', value=datetime.date(2024, 1, 1))
edate = st.sidebar.date_input('End Date', value=datetime.date.today())

# Main title
st.title(f"{symbol} Stock Analysis")

# Fetch the stock data
stock = yf.Ticker(symbol)
data = stock.history(start=sdate, end=edate)

# Display stock details if data is available
if not data.empty:
    # Company information
    st.subheader(f"Company Information for {symbol}")
    st.write(f"**Sector**: {stock.info.get('sector', 'N/A')}")
    st.write(f"**Beta**: {stock.info.get('beta', 'N/A')}")
    
    # Stock data overview
    st.subheader("Stock Data Summary")
    st.write(data.describe())

    # Plot Closing Price chart
    st.subheader("Closing Price Over Time")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name="Close Price"))
    fig.update_layout(xaxis_title="Date", yaxis_title="Closing Price (USD)")
    st.plotly_chart(fig)
else:
    st.error("Failed to fetch historical data for this stock.")

# Market Overview Section
st.header("Global Markets Overview")

# Display selected indices
indices = {
    "S&P 500": "^GSPC",
    "Dow Jones": "^DJI",
    "Nasdaq": "^IXIC",
    "FTSE 100": "^FTSE",
    "Nikkei 225": "^N225",
    "Hang Seng": "^HSI"
}

index_data = {}
for name, symbol in indices.items():
    index = yf.Ticker(symbol)
    index_info = index.history(period="1d")
    index_data[name] = index_info["Close"][-1]

# Display indices in a column format
for name, price in index_data.items():
    st.metric(label=name, value=f"${price:.2f}")

# Currency Exchange Rates
st.subheader("Currency Exchange Rates")
currencies = ["USDJPY=X", "EURUSD=X", "GBPUSD=X"]
currency_data = {}
for currency in currencies:
    currency_ticker = yf.Ticker(currency)
    currency_info = currency_ticker.history(period="1d")
    currency_data[currency] = currency_info["Close"][-1]

for currency, price in currency_data.items():
    st.metric(label=currency.replace("=X", ""), value=f"${price:.2f}")

# Commodity Prices
st.subheader("Commodities")
commodities = {
    "Gold": "GC=F",
    "Silver": "SI=F",
    "Crude Oil": "CL=F"
}
commodity_data = {}
for name, symbol in commodities.items():
    commodity = yf.Ticker(symbol)
    commodity_info = commodity.history(period="1d")
    commodity_data[name] = commodity_info["Close"][-1]

for name, price in commodity_data.items():
    st.metric(label=name, value=f"${price:.2f}")

# Cryptocurrency Data
st.subheader("Cryptocurrencies")
cryptos = ["BTC-USD", "ETH-USD", "ADA-USD"]
crypto_data = {}
for crypto in cryptos:
    crypto_ticker = yf.Ticker(crypto)
    crypto_info = crypto_ticker.history(period="1d")
    crypto_data[crypto] = crypto_info["Close"][-1]

for crypto, price in crypto_data.items():
    st.metric(label=crypto.replace("-USD", ""), value=f"${price:.2f}")

# Display Market News (Yahoo Finance scraping example)
st.subheader("Latest Financial News")

def fetch_yahoo_finance_news():
    url = "https://finance.yahoo.com/markets"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        news_items = soup.find_all("h3", {"class": "Mb(5px)"})[:5]  # Get top 5 news
        news = []
        for item in news_items:
            title = item.get_text()
            link = "https://finance.yahoo.com" + item.find("a")["href"]
            news.append((title, link))
        return news
    else:
        return []

news = fetch_yahoo_finance_news()
if news:
    for title, link in news:
        st.write(f"[{title}]({link})")
else:
    st.write("Failed to fetch news.")

# Economic Events Calendar (Mock Data as Example)
st.subheader("Upcoming Economic Events")
events = [
    {"Date": "2024-01-15", "Event": "US Retail Sales"},
    {"Date": "2024-01-18", "Event": "ECB Interest Rate Decision"},
    {"Date": "2024-01-24", "Event": "Japan CPI Release"},
]
for event in events:
    st.write(f"{event['Date']}: {event['Event']}")
