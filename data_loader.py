import yfinance as yf
import pandas as pd
import streamlit as st

def load_data(ticker, start_date, end_date):
    """
    Loads stock data from Yahoo Finance for a single ticker and date range.

    Args:
        ticker (str): Stock ticker symbol.
        start_date (str): Start date in YYYY-MM-DD format.
        end_date (str): End date in YYYY-MM-DD format.

    Returns:
        pandas.DataFrame: DataFrame containing stock data for the ticker.
    """
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
        # Flatten the MultiIndex columns
        data.columns = data.columns.droplevel(1)  # Drop the second level (ticker name)
        data.columns.name = None  # Remove the column name

        if data is None or data.empty:
            st.error(f"No data found for ticker: {ticker}")
            return None

        return data

    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None
