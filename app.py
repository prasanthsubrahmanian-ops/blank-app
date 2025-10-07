  import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf

st.set_page_config(page_title="Prasanth AI Trader", page_icon="📈", layout="wide")

st.title("📊 Welcome to Prasanth AI Trader")
st.markdown("#### Real-time NIFTY 50 Stocks Analytics 🚀")

# Sidebar for stock selection
nifty_symbols = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK",
                 "SBIN", "HINDUNILVR", "LT", "AXISBANK", "ITC"]
symbol = st.sidebar.selectbox("Select Stock", nifty_symbols)

# Fetch live stock data from Yahoo Finance
st.subheader(f"📈 Live Price for {symbol}")
ticker = yf.Ticker(symbol + ".NS")
data = ticker.history(period="1d")

if data.empty:
    st.warning("No live data available.")
else:
    st.dataframe(data.tail(1))

# Display candlestick chart for past 1 month
st.subheader(f"{symbol} Candlestick Chart (1 Month)")
hist = ticker.history(period="1mo")

if not hist.empty:
    hist.reset_index(inplace=True)
    fig = go.Figure(data=[go.Candlestick(
        x=hist['Date'],
        open=hist['Open'],
        high=hist['High'],
        low=hist['Low'],
        close=hist['Close']
    )])
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Price (INR)",
        xaxis_rangeslider_visible=False,
        template="plotly_dark"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No chart data available.")

st.markdown("---")
st.caption("📈 Developed by Prasanth | Cloud Safe AI Trader Dashboard")                 
