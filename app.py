# app.py - Prasanth AI Trader Dashboard (Safe & Interactive)
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from nsepython import get_quote, nse_optionchain_scrapper, nse_expiry_dates
import yfinance as yf

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Prasanth AI Trader",
    page_icon="📈",
    layout="wide"
)

# -----------------------------
# Header
# -----------------------------
st.title("📊 Welcome to Prasanth AI Trader")
st.markdown("#### Real-time NIFTY 50 & Bank NIFTY Stocks & Options Analytics 🚀")

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("Select Options")
index_option = st.sidebar.selectbox("Select Index", ["NIFTY 50", "BANK NIFTY"])

nifty_symbols = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK",
                 "SBIN", "HINDUNILVR", "LT", "AXISBANK", "ITC"]
symbol = st.sidebar.selectbox("Select Stock", nifty_symbols)

# Option expiry dates (safe fetch)
try:
    expiries = nse_expiry_dates()
except Exception as e:
    expiries = []
    st.warning(f"Could not fetch expiry dates: {e}")

if expiries:
    expiry = st.sidebar.selectbox("Option Expiry", expiries)
else:
    expiry = st.sidebar.text_input("Option Expiry (enter manually)", "2025-10-10")

# -----------------------------
# Live Stock Quote (NSEPython + fallback)
# -----------------------------
st.subheader(f"Live Price for {symbol}")
try:
    quote = get_quote(symbol)
    if quote:
        quote_df = pd.DataFrame([quote]).T
        quote_df.columns = ["Value"]
        st.dataframe(quote_df)
    else:
        # Fallback to yfinance
        ticker = yf.Ticker(symbol + ".NS")
        data = ticker.history(period="1d")
        st.dataframe(data.tail(1))
except Exception:
    try:
        ticker = yf.Ticker(symbol + ".NS")
        data = ticker.history(period="1d")
        st.dataframe(data.tail(1))
    except Exception as e2:
        st.error(f"Cannot fetch data for {symbol}: {e2}")

# -----------------------------
# Candlestick Chart
# -----------------------------
st.subheader(f"{symbol} Candlestick Chart (Daily OHLC)")
try:
    ticker = yf.Ticker(symbol + ".NS")
    hist = ticker.history(period="1mo")
    if not hist.empty:
        hist.reset_index(inplace=True)
        fig = go.Figure(data=[go.Candlestick(
            x=hist['Date'],
            open=hist['Open'],
            high=hist['High'],
            low=hist['Low'],
            close=hist['Close'],
            name=symbol
        )])
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Price (INR
