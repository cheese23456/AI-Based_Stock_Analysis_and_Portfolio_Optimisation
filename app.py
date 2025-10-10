import streamlit as st
import pandas as pd
import plotly.express as px
from data_loader import load_data
from indicators import calculate_indicators
from ai_insights import get_ai_insight
from portfolio_optimiser import optimize_portfolio
import os

# Streamlit UI
st.title("AI-Powered Stock Analysis and Portfolio Optimisation Tool")

# User Inputs
tickers = st.text_input("Enter stock tickers (comma-separated, e.g., TSLA, AAPL, MSFT):", "")
tickers = [ticker.strip().upper() for ticker in tickers.split(",")]

start_date = st.date_input("Start Date:", value=pd.to_datetime("2024-01-01"))
end_date = st.date_input("End Date:", value=pd.to_datetime("2025-01-01"))

ma_window = st.slider("Moving Average Window:", min_value=5, max_value=50, value=20)
rsi_window = st.slider("RSI Window:", min_value=5, max_value=30, value=14)
macd_fast = st.slider("MACD Fast Period:", min_value=5, max_value=30, value=12)
macd_slow = st.slider("MACD Slow Period:", min_value=20, max_value=50, value=26)
macd_signal = st.slider("MACD Signal Period:", min_value=5, max_value=20, value=9)

risk_tolerance = st.slider("Risk Tolerance (0-1):", min_value=0.0, max_value=1.0, value=0.5, step=0.01)


def calculate_and_return_everything(data):
    # Calculate Indicators
    indicator_data = calculate_indicators(data, ma_window, rsi_window, macd_fast, macd_slow, macd_signal)
    if indicator_data is None:
        st.stop()

    # AI Insights
    st.subheader("💡 AI Insights")
    last_row = indicator_data.iloc[-1]

    api_key = st.secrets["OPENAI_API_KEY"]  # Ensure API key is set

    # Get AI insights for each indicator
    ma_insight = get_ai_insight("Moving Average", last_row['MA'], api_key)
    bb_insight = get_ai_insight("Bollinger Bands", f"Upper: {last_row['Upper_BB']}, Lower: {last_row['Lower_BB']}", api_key)
    rsi_insight = get_ai_insight("RSI", last_row['RSI'], api_key)
    macd_insight = get_ai_insight("MACD", last_row['MACD'], api_key)

    st.write(f"Moving Average: {ma_insight}")
    st.write(f"Bollinger Bands: {bb_insight}")
    st.write(f"RSI: {rsi_insight}")
    st.write(f"MACD: {macd_insight}")


    # ---- Investment Signal (clear signage) ----
    ma = float(last_row['MA'])
    close_price = float(last_row['Close'])
    rsi = float(last_row['RSI'])
    macd = float(last_row['MACD'])
    lower_bb = float(last_row['Lower_BB'])
    upper_bb = float(last_row['Upper_BB'])

    st.write(f"Moving Average Value: {ma}")
    st.write(f"Closing Price: {close_price}")
    st.write(f"Lower Bollinger Band: {lower_bb}")
    st.write(f"Upper Bollinger Band: {upper_bb}")
    st.write(f"RSI Value: {rsi}")
    st.write(f"MACD Value: {macd}")

    
    return indicator_data



if st.button("Analyse"):
    all_data = {}
    for i in tickers:
        # Load Data
        data = load_data(i, start_date, end_date) # Passing ticker instead of tickers
        if data is None:
            st.warning(f"No data found for {i}. Skipping...")
            continue
        st.subheader(f'Ticker: {i}')
        id = calculate_and_return_everything(data)
        if id is not None:
            all_data[i] = id

    if not all_data:
        st.warning("No valid data available for any of the tickers. Exiting analysis.")
        st.stop()

    # Portfolio Optimisation
    st.subheader("Portfolio Optimisation")

    # Extract closing prices for portfolio optimization
    close_prices = pd.DataFrame({ticker: all_data[ticker]['Close'] for ticker in all_data})

    print(close_prices.columns)

    asset_weights = optimize_portfolio(close_prices, risk_tolerance)
    if asset_weights:
        st.write("### Optimised Asset Allocation:")
        for ticker, weight in asset_weights.items():
            st.write(f"**{ticker}:** {weight:.4f}")
    else:
        st.write("Could not perform portfolio optimisation.")

print("Ensure that you have your OpenAI API set as environmental variable in Hugging Face Spaces for this script to work")
