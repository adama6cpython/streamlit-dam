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

# Stocks Overview Section
st.header("Stocks Overview")

# Mock-up lists for Most Active, Trending Now, Top Gainers, Top Losers, 52-Week Gainers, and 52-Week Losers
# Replace these with API data or scraping results as needed
mock_data = {
    "Most Active": ["AAPL", "TSLA", "NVDA", "MSFT", "AMD"],
    "Trending Now": ["AMZN", "META", "NFLX", "GOOGL", "BABA"],
    "Top Gainers": ["SNAP", "RKT", "CRSP", "ZM", "SPCE"],
    "Top Losers": ["COIN", "PLTR", "FUBO", "BBBY", "GME"],
    "52-Week Gainers": ["NVDA", "TSLA", "AAPL", "AMZN", "GOOGL"],
    "52-Week Losers": ["DIS", "T", "CMCSA", "WBA", "INTC"]
}

# Function to display stock data for each category
def display_stock_list(category, symbols):
    st.subheader(category)
    for sym in symbols:
        ticker = yf.Ticker(sym)
        info = ticker.info
        price = info.get("regularMarketPrice", "N/A")
        day_low = info.get("dayLow", "N/A")
        day_high = info.get("dayHigh", "N/A")
        fifty_two_week_low = info.get("fiftyTwoWeekLow", "N/A")
        fifty_two_week_high = info.get("fiftyTwoWeekHigh", "N/A")
        volume = info.get("volume", "N/A")
        market_cap = info.get("marketCap", "N/A")
        
        # Display stock info in columns
        col1, col2, col3, col4 = st.columns(4)
        col1.metric(label=f"{sym} - {info.get('shortName', sym)}", value=f"${price}")
        col2.write(f"**Day Range**: {day_low} - {day_high}")
        col3.write(f"**52-Week Range**: {fifty_two_week_low} - {fifty_two_week_high}")
        col4.write(f"**Volume**: {volume} | **Market Cap**: {market_cap}")

# Display each stock category
for category, symbols in mock_data.items():
    display_stock_list(category, symbols)

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
