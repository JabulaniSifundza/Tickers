import pandas as pd
import streamlit as st
import yfinance as yf

st.title ("Stock Visualization App")
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
