# app.py - Prasanth AI Trader Dashboard (Safe Version)
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from nsepython import get_quote, nse_optionchain_scrapper, nse_expiry_dates
from datetime import datetime

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
# Sidebar for Inputs
# -----------------------------
st.sidebar.header("Select Options")
index_option = st.sidebar.selectbox("Select Index", ["NIFTY 50", "BANK NIFTY"])

# Example NIFTY 50 stocks
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
# Live Stock Quote
# -----------------------------
st.subheader(f"Live Price for {symbol}")
try:
    quote = get_quote(symbol)
    quote_df = pd.DataFrame([quote]).T
    quote_df.columns = ["Value"]
    st.dataframe(quote_df)
except Exception as e:
    st.error(f"Error fetching live stock data: {e}")

# -----------------------------
# Candlestick Chart (Daily OHLC)
# -----------------------------
st.subheader(f"{symbol} Candlestick Chart (Daily OHLC)")
try:
    hist = quote['history'] if 'history' in quote else None
    if hist:
        hist_df = pd.DataFrame(hist)
        hist_df['Date'] = pd.to_datetime(hist_df['Date'])
        hist_df = hist_df.sort_values('Date')
        fig = go.Figure(data=[go.Candlestick(
            x=hist_df['Date'],
            open=hist_df['Open'],
            high=hist_df['High'],
            low=hist_df['Low'],
            close=hist_df['Close'],
            name=symbol
        )])
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Price (INR)",
            xaxis_rangeslider_visible=False,
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Historical OHLC data not available.")
except Exception as e:
    st.error(f"Error fetching OHLC data: {e}")

# -----------------------------
# NIFTY Option Chain
# -----------------------------
if index_option == "NIFTY 50":
    st.subheader(f"NIFTY Option Chain for Expiry: {expiry}")
    try:
        option_chain = nse_optionchain_scrapper('NIFTY', expiry)
        ce_data = pd.DataFrame(option_chain.get('CE', []))
        pe_data = pd.DataFrame(option_chain.get('PE', []))

        if not ce_data.empty:
            st.markdown("**Call Options (CE)**")
            st.dataframe(ce_data.head(20))
        else:
            st.info("Call Options data not available.")

        if not pe_data.empty:
            st.markdown("**Put Options (PE)**")
            st.dataframe(pe_data.head(20))
        else:
            st.info("Put Options data not available.")

    except Exception as e:
        st.warning(f"Could not fetch NIFTY option chain: {e}")

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.caption("📈 Developed by Prasanth | AI-Powered NIFTY Trade Dashboard")
