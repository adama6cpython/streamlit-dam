import streamlit as st
import yfinance as yf
import datetime
import plotly.graph_objs as go
import requests
import pandas as pd

# Set up the page configuration and title
st.set_page_config(layout="wide", page_title="Market Overview and Economic Data Analysis")

# Sidebar for stock selection and date range
st.sidebar.title("Stock Analysis")
symbol = st.sidebar.text_input('Enter stock symbol (e.g., NVDA, AAPL):', 'NVDA').upper()
sdate = st.sidebar.date_input('Start Date', value=datetime.date(2024, 1, 1))
edate = st.sidebar.date_input('End Date', value=datetime.date.today())

# Main title for stock analysis
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

# Economic Data Section: GDP Analysis
st.header("Global Economic Data: GDP Analysis")

# World Bank API endpoint for GDP data
WORLD_BANK_API_URL = "http://api.worldbank.org/v2/country/{}/indicator/NY.GDP.MKTP.CD?format=json&date=1960:2022"

# Country codes for selection
country_codes = {
    "United States": "USA",
    "China": "CHN",
    "Japan": "JPN",
    "Germany": "DEU",
    "France": "FRA",
    "United Kingdom": "GBR",
    "Brazil": "BRA",
    "Mexico": "MEX",
    "India": "IND"
}

# Multiselect for countries
selected_countries = st.multiselect("Which countries would you like to view?", list(country_codes.keys()), default=["United States", "China"])

# Function to fetch GDP data for a list of countries
def fetch_gdp_data(countries):
    gdp_data = {}
    for country in countries:
        code = country_codes[country]
        response = requests.get(WORLD_BANK_API_URL.format(code))
        if response.status_code == 200:
            data = response.json()[1]
            gdp_data[country] = pd.DataFrame(data)[["date", "value"]].rename(columns={"date": "Year", "value": "GDP"}).set_index("Year").sort_index()
    return gdp_data

# Fetch GDP data for selected countries
gdp_data = fetch_gdp_data(selected_countries)

# Display GDP over time
st.subheader("GDP Over Time")
if gdp_data:
    # Combine data for plotting
    combined_df = pd.concat(gdp_data.values(), keys=gdp_data.keys(), axis=1)
    combined_df.columns = [f"{country} GDP" for country in gdp_data.keys()]

    # Plot the GDP data
    fig = go.Figure()
    for country in gdp_data.keys():
        fig.add_trace(go.Scatter(x=combined_df.index, y=combined_df[f"{country} GDP"], mode='lines', name=country))
    fig.update_layout(xaxis_title="Year", yaxis_title="GDP (Current US$)")
    st.plotly_chart(fig)

    # Display GDP in the most recent year (2022 if available)
    st.subheader("GDP in the Most Recent Year")
    latest_year = combined_df.index[-1]
    latest_gdp = combined_df.loc[latest_year]
    for country, gdp in latest_gdp.items():
        st.metric(label=f"{country} GDP ({latest_year})", value=f"${gdp:,.0f}")

else:
    st.write("No data available for the selected countries.")

# Market Overview Section (continuation from the previous code)
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
