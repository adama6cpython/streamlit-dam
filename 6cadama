# stock_app.py
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

st.markdown(
    """
    <style>
    body {
        background-color: orange;
        color: white;

    }
    .stTextInput, .stDateInput, .stSelectbox, .stRadio, .stCheckbox, .stSlider {
        color: yellow !important;
    }
    .stButton>button {
        background-cols as go
from datetime import datetime

# Custom CSS for background color and text color
st.markdown(or: yellow;
        color: black;
    }
    </style>
    """, unsafe_allow_html=True
)

# Set title and description
st.title("Stock Information Web App")
st.write("Enter a ticker symbol to retrieve and visualize stock information interactively.")

# Get the ticker symbol input
ticker_symbol = st.text_input("Enter stock ticker (e.g., AAPL, MSFT):", "AAPL")

# Date input for custom date range
start_date = st.date_input("Start Date", value=datetime(2022, 1, 1))
end_date = st.date_input("End Date", value=datetime.now())

# Ensure end date is not earlier than start date
if start_date > end_date:
    st.error("End date must be after the start date. Please adjust your dates.")
else:
    if ticker_symbol:
        try:
            # Get stock data from yfinance
            stock = yf.Ticker(ticker_symbol)

            # Display basic information
            st.subheader("Company Information")
            info = stock.info
            st.write(f"**Name**: {info.get('longName', 'N/A')}")
            st.write(f"**Sector**: {info.get('sector', 'N/A')}")
            st.write(f"**Industry**: {info.get('industry', 'N/A')}")
            st.write(f"**Country**: {info.get('country', 'N/A')}")

            # Display current stock price
            st.subheader("Stock Price")
            st.write(f"**Current Price**: ${info.get('currentPrice', 'N/A')}")
            st.write(f"**Market Cap**: ${info.get('marketCap', 'N/A')}")
            st.write(f"**PE Ratio**: {info.get('trailingPE', 'N/A')}")

            # Fetch historical data within selected date range
            st.subheader("Historical Data")

            # Select interval for data
            interval = st.selectbox("Select Interval", ["1d", "5d", "1wk", "1mo", "3mo"])
            data = stock.history(start=start_date, end=end_date, interval=interval)
            st.write(data.tail())

            # Option to display moving averages
            show_moving_average = st.checkbox("Show Moving Averages")
            if show_moving_average:
                # Allow user to select two different moving average periods
                short_ma_period = st.slider("Select Short-Term Moving Average Period (days)", 5, 50, 20)
                long_ma_period = st.slider("Select Long-Term Moving Average Period (days)", 50, 200, 100)

                # Calculate short-term and long-term moving averages
                data[f"SMA_{short_ma_period}"] = data['Close'].rolling(short_ma_period).mean()
                data[f"SMA_{long_ma_period}"] = data['Close'].rolling(long_ma_period).mean()

            # Option to select chart type
            chart_type = st.radio("Select Chart Type", ["Line Chart", "Candlestick Chart"])

            # Display the selected chart
            if chart_type == "Line Chart":
                st.subheader("Stock Price Over Time - Line Chart")
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name="Close Price"))

                # Add short-term and long-term moving averages to the line chart if enabled
                if show_moving_average:
                    fig.add_trace(go.Scatter(x=data.index, y=data[f"SMA_{short_ma_period}"],
                                             mode='lines', name=f"SMA {short_ma_period}"))
                    fig.add_trace(go.Scatter(x=data.index, y=data[f"SMA_{long_ma_period}"],
                                             mode='lines', name=f"SMA {long_ma_period}"))

                fig.update_layout(title=f"{ticker_symbol} Closing Prices",
                                  xaxis_title="Date", yaxis_title="Price (USD)")
                st.plotly_chart(fig)

            elif chart_type == "Candlestick Chart":
                st.subheader("Stock Price Over Time - Candlestick Chart")
                fig = go.Figure(data=[go.Candlestick(
                    x=data.index,
                    open=data['Open'],
                    high=data['High'],
                    low=data['Low'],
                    close=data['Close'],
                )])

                # Add short-term and long-term moving averages to the candlestick chart if enabled
                if show_moving_average:
                    fig.add_trace(go.Scatter(x=data.index, y=data[f"SMA_{short_ma_period}"],
                                             mode='lines', name=f"SMA {short_ma_period}"))
                    fig.add_trace(go.Scatter(x=data.index, y=data[f"SMA_{long_ma_period}"],
                                             mode='lines', name=f"SMA {long_ma_period}"))

                fig.update_layout(
                    title=f"Candlestick chart for {ticker_symbol}",
                    xaxis_title="Date",
                    yaxis_title="Price (USD)",
                    xaxis_rangeslider_visible=False
                )
                st.plotly_chart(fig)

        except Exception as e:
            st.error(f"Could not retrieve data for {ticker_symbol}. Error: {e}")
