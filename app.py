import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(page_title="AI Trader", layout="wide")

st.title("📈 AI Trader Dashboard")
st.write("Welcome to your AI-powered trading insights app!")

# Sidebar input
symbol = st.sidebar.text_input("Enter Stock Symbol (e.g. AAPL, RELIANCE.NS):", "RELIANCE.NS")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2024-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))

# Fetch data
try:
    data = yf.download(symbol, start=start_date, end=end_date)
    if data.empty:
        st.warning("No data found for this symbol.")
    else:
        st.subheader(f"{symbol} Stock Data")
        st.dataframe(data.tail())

        # Chart
        fig = go.Figure()
        fig.add_trace(go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name="Candlestick"
        ))
        fig.update_layout(title=f"{symbol} Price Chart", xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)
except Exception as e:
    st.error(f"Error loading data: {e}")

st.write("Developed by Prasanth’s AI Trader 🧠💹")
