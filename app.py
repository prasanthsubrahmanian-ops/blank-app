import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Trading Analysis App", layout="wide")

st.title("📈 Trading Analysis Web App")
st.write("Analyze stock data, visualize trends, and download reports easily.")

# Input section
ticker = st.text_input("Enter Stock Symbol (e.g., TCS.NS, RELIANCE.NS, INFY.NS):", "TCS.NS")

# Fetch data
data = yf.download(ticker, period="6mo", interval="1d")

if not data.empty:
    st.subheader(f"Showing data for: {ticker}")
    st.dataframe(data.tail())

            # Plot closing price
                fig = go.Figure()
                    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close Price'))
                        fig.update_layout(title=f"{ticker} Closing Price", xaxis_title="Date", yaxis_title="Price")
                            st.plotly_chart(fig, use_container_width=True)

                                # Basic statistics
                                    st.subheader("📊 Key Statistics")
                                        st.write(f"**Average Close:** {data['Close'].mean():.2f}")
                                            st.write(f"**Highest Close:** {data['Close'].max():.2f}")
                                                st.write(f"**Lowest Close:** {data['Close'].min():.2f}")

                                                    # Download data
                                                        csv = data.to_csv().encode('utf-8')
                                                            st.download_button("📥 Download CSV", csv, f"{ticker}_data.csv", "text/csv")

                                                            else:
                                                                st.error("No data found. Please enter a valid stock symbol (e.g., TCS.NS or INFY.NS).")
