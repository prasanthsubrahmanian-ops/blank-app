# app.py - AI NIFTY Trade Dashboard
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Trade Dashboard - NIFTY",
    page_icon="📈",
    layout="wide"
)

# -----------------------------
# Header
# -----------------------------
st.title("📊 Welcome to the AI Trade Dashboard")
st.markdown("#### Real-time NIFTY 50 & Bank NIFTY Stocks & Derivatives Analytics 🚀")

# -----------------------------
# Sidebar for User Inputs
# -----------------------------
st.sidebar.header("Select Options")

index_option = st.sidebar.selectbox("Select Index", ["NIFTY 50", "BANK NIFTY"])

# Example NIFTY 50 stocks (you can expand later)
nifty_symbols = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS",
    "ICICIBANK.NS", "SBIN.NS", "HINDUNILVR.NS",
    "LT.NS", "AXISBANK.NS", "ITC.NS"
]

symbol = st.sidebar.selectbox("Select Stock", nifty_symbols)
period = st.sidebar.selectbox("Period", ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y"])
interval = st.sidebar.selectbox("Interval", ["5m", "15m", "1h", "1d"])

# -----------------------------
# Fetch Data
# -----------------------------
st.info(f"Fetching data for **{symbol}**...")

try:
    data = yf.download(symbol, period=period, interval=interval)
    data.reset_index(inplace=True)

    # -----------------------------
    # Plotly Candlestick Chart
    # -----------------------------
    fig = go.Figure(data=[go.Candlestick(
        x=data['Datetime'] if 'Datetime' in data.columns else data['Date'],
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name=symbol
    )])

    fig.update_layout(
        title=f"{symbol} Price Chart ({period})",
        xaxis_title="Date",
        yaxis_title="Price (INR)",
        xaxis_rangeslider_visible=False,
        template="plotly_dark"
    )

    st.plotly_chart(fig, use_container_width=True)

    # -----------------------------
    # Display Latest Data
    # -----------------------------
    st.subheader("Recent Data")
    st.dataframe(data.tail(10))

except Exception as e:
    st.error(f"Error fetching data: {e}")

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.caption("📈 Developed by Prasanth | AI-Powered NIFTY Trade Dashboard")
