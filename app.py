# app.py - Prasanth AI Trader Dashboard (Safe for Streamlit Cloud)
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from nsepython import nse_optionchain_scrapper, nse_expiry_dates
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
# Live Stock Quote (yfinance only)
# -----------------------------
st.subheader(f"Live Price for {symbol}")
try:
    ticker = yf.Ticker(symbol + ".NS")
    data = ticker.history(period="1d")
    if not data.empty:
        latest = data.tail(1)
        st.dataframe(latest)
    else:
        st.warning("No data available for this stock.")
except Exception as e:
    st.error(f"Cannot fetch data for {symbol}: {e}")

# -----------------------------
# Candlestick Chart (1 month)
# -----------------------------
st.subheader(f"{symbol} Candlestick Chart (1 Month OHLC)")
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
            yaxis_title="Price (INR)",
            xaxis_rangeslider_visible=False,
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Candlestick data not available.")
except Exception as e:
    st.error(f"Error fetching candlestick data: {e}")

# -----------------------------
# NIFTY Option Chain Visualization
# -----------------------------
if index_option == "NIFTY 50":
    st.subheader(f"NIFTY Option Chain for Expiry: {expiry}")
    try:
        option_chain = nse_optionchain_scrapper('NIFTY', expiry)
        ce_data = pd.DataFrame(option_chain.get('CE', []))
        pe_data = pd.DataFrame(option_chain.get('PE', []))

        if not ce_data.empty and not pe_data.empty:
            # Plot Strike Price vs Open Interest
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=ce_data['strikePrice'],
                y=ce_data['openInterest'],
                name='Call OI',
                marker_color='green',
                opacity=0.7
            ))
            fig.add_trace(go.Bar(
                x=pe_data['strikePrice'],
                y=pe_data['openInterest'],
                name='Put OI',
                marker_color='red',
                opacity=0.7
            ))
            fig.update_layout(
                title=f"NIFTY Options Open Interest (Expiry: {expiry})",
                xaxis_title="Strike Price",
                yaxis_title="Open Interest",
                barmode='group',
                template="plotly_dark"
            )
            st.plotly_chart(fig, use_container_width=True)

            # Top 10 CE & PE tables
            st.markdown("**Top 10 Call Options (CE)**")
            st.dataframe(ce_data.head(10))
            st.markdown("**Top 10 Put Options (PE)**")
            st.dataframe(pe_data.head(10))
        else:
            st.info("Option chain data not available.")
    except Exception as e:
        st.warning(f"Could not fetch NIFTY option chain: {e}")

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.caption("📈 Developed by Prasanth | AI-Powered NIFTY Trade Dashboard")
