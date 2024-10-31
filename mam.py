import streamlit as st
import matplotlib.pyplot as plt
import datetime
import plotly.graph_objs as go
import appdirs as ad
ad.user_cache_dir = lambda *args: "/tmp"
import yfinance as yf
# Title of the app
st.title("Financial Information App")

# Input for stock ticker
ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, GOOGL):")

if ticker:
    # Fetching stock data
    stock_data = yf.Ticker(ticker)

    # Fetching the current price and other financial metrics
    st.subheader(f"Current Price of {ticker}:")
    try:
        price = stock_data.history(period='1d')['Close'][0]
        st.write(f"💵 **Current Price:** ${price:.2f}")

        # Displaying additional financial metrics
        st.subheader("Financial Metrics:")
        info = stock_data.info
        metrics = {
            "Market Cap": info.get('marketCap', 'N/A'),
            "PE Ratio": info.get('trailingPE', 'N/A'),
            "Dividend Yield": info.get('dividendYield', 'N/A'),
            "52 Week High": info.get('fiftyTwoWeekHigh', 'N/A'),
            "52 Week Low": info.get('fiftyTwoWeekLow', 'N/A'),
        }

        for metric, value in metrics.items():
            st.write(f"{metric}: {value}")

    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {e}")
