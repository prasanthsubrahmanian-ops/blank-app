import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="Prashu AI Trader", layout="wide")

st.title("📊 Prashu – Simple NIFTY Dashboard")
st.write("Track NIFTY 50 stocks and index charts easily")

# --- Stock Selection ---
stocks = ["RELIANCE", "TCS", "INFY", "ICICIBANK", "HDFCBANK"]
selected = st.selectbox("Select Stock", stocks)

# --- Fetch Data ---
data = yf.download(f"{selected}.NS", period="1mo", interval="1d")
if data.empty:
    st.warning("No data found. Try another stock.")
else:
    data.reset_index(inplace=True)
    st.subheader(f"{selected} - Last 5 Days")
    st.dataframe(data.tail())

    fig = go.Figure(data=[go.Candlestick(
        x=data['Date'],
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close']
    )])
    fig.update_layout(
        title=f"{selected} - Candlestick Chart",
        xaxis_rangeslider_visible=False,
        template="plotly_dark"
    )
    st.plotly_chart(fig, use_container_width=True)

# --- NIFTY Index ---
st.subheader("NIFTY 50 Index Chart")
nifty = yf.download("^NSEI", period="1mo", interval="1d")

if not nifty.empty:
    nifty.reset_index(inplace=True)
    fig2 = go.Figure(data=[go.Candlestick(
        x=nifty['Date'],
        open=nifty['Open'],
        high=nifty['High'],
        low=nifty['Low'],
        close=nifty['Close']
    )])
    fig2.update_layout(
        title="NIFTY 50 Index",
        xaxis_rangeslider_visible=False,
        template="plotly_dark"
    )
    st.plotly_chart(fig2, use_container_width=True)
