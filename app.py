import pandas as pd
import streamlit as st
import yfinance as yf
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np 


st.title ("Stock Visualization App")
st.subheader("Individual company stock information")
st.write("Please enter a ticker symbol to begin visualizing")
tickerSymbol = st.text_input("Enter the ticker symbol 👇🏾", placeholder="Ticker symbol")
if len(tickerSymbol) < 1:
    st.write("Please enter a ticker symbol to start")
else:
    st.subheader(f"Showing {tickerSymbol} stock information")
    # tickerSymbol = 'AAPL'
    # Get data on ticker
    symbolData = yf.Ticker(tickerSymbol)
    symbolDf = symbolData.history(period='1d', start='2010-1-31', end='2022-12-31')
    st.write("Dividends per share")
    st.line_chart(symbolDf.Dividends)
    st.markdown("Highs")
    st.line_chart(symbolDf.High)
    st.write("Closing Price")
    st.line_chart(symbolDf.Close)
    st.write("Trading Volume")
    st.line_chart(symbolDf.Volume)
    
# S&P 500 companies
st.title("S&P 500 Companies")
st.markdown("""
All company info is retrieved from Wikipedia S&P 500 page
* **Data source:** [Wikipedia](https://www.wikipedia.org/).
""")

st.sidebar.header("User Input Features")

# Web scraping data from wikipedia
@st.cache
def load_data():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    html = pd.read_html(url, header=0)
    return html[0]

df1 = load_data()
sector = df1.groupby('GICS Sector')
# Isolating sectors from dataframe
unique_sector = sorted(df1['GICS Sector'].unique())
selected_sector = st.sidebar.multiselect('Sector', unique_sector)
# Filtering Data 
df1_selected_sector = df1[(df1['GICS Sector'].isin(selected_sector))]
st.subheader("Show companies in selected sector")
st.dataframe(df1_selected_sector)
# Download data
def download_file(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f"<a href='data:file/csv;base64,{b64}' download='SP500.CSV'>Download Data</a>"

st.markdown(download_file(df1_selected_sector), unsafe_allow_html=True)
    
# Grouping data by sector
# sector.describe()
# sector.get_group('Financial')
# list(df1.Symbol)

if len(df1_selected_sector) < 1:
    st.subheader("Please select a company sector to start")
else:
    stock_data = yf.download(
    tickers = list(df1_selected_sector[:25].Symbol),
    period = "ytd",
    interval = "1d",
    group_by= "ticker",
    auto_adjust = True,
    prepost= True,
    threads= True,
    proxy = None
)
# tickerSymbol2 = st.text_input("Enter the ticker symbol 👇🏾", placeholder="Ticker symbol")
# df2 = pd.DataFrame(stock_data[Symbol].close)
# df2['Date'] = df2.index
# plt.fill_between(df2.Date, df2.Close, color='green', alpha=0.3)
# plt.plot(df2.Date, df2.Close, color='green', alpha = 0.8)
# plt.xticks(rotation=90)
# plt.xlabel("Date")
# plt.ylabel("Closing Price")
def price_plot(symbol):
    df2 = pd.DataFrame(stock_data[symbol].Close)
    df2['Date'] = df2.index
    fig, ax = plt.subplots()
    ax = plt.fill_between(df2.Date, df2.Close, color='green', alpha=0.3)
    ax = plt.plot(df2.Date, df2.Close, color='green', alpha = 0.8)
    ax = plt.xticks(rotation=90)
    ax = plt.xlabel("Date", fontweight='bold')
    ax = plt.ylabel("Closing Price", fontweight='bold')
    ax = plt.title(symbol, fontweight='bold')
    return st.pyplot(fig)
# for i in list(df1.Symbol)[:10]:
    # price_plot(i)

num_company = st.sidebar.slider('Number of Companies', 1, 40)
if st.button('Show Plots'):
    st.header('Stock Closing Price')
    for i in list(df1_selected_sector.Symbol)[:num_company]:
        price_plot(i)
    