import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
import streamlit as st
from ai_insights import get_ai_insight

def calculate_indicators(data, ma_window, rsi_window, macd_fast, macd_slow, macd_signal):
    """
    Calculates Moving Average (MA), Bollinger Bands, RSI, MACD, and displays them in a 2x2 grid in Streamlit.
    Also includes AI-generated insights next to each chart.

    Args:
        data (pandas.DataFrame): Stock data.
        ma_window (int): Moving Average window.
        rsi_window (int): RSI window.
        macd_fast (int): MACD Fast period.
        macd_slow (int): MACD Slow period.
        macd_signal (int): MACD Signal period.

    Returns:
        pandas.DataFrame: Data with calculated indicators.
    """

    # Calculate Moving Average (MA)
    data['MA'] = data['Close'].rolling(window=ma_window).mean()

    # Calculate Bollinger Bands
    data['stddev'] = data['Close'].rolling(window=ma_window).std()
    data['Upper_BB'] = data['MA'] + (2 * data['stddev'])
    data['Lower_BB'] = data['MA'] - (2 * data['stddev'])

    # Calculate RSI
    delta = data['Close'].diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=rsi_window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=rsi_window).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))

    # Calculate MACD
    data['MACD'] = data['Close'].ewm(span=macd_fast, adjust=False).mean() - data['Close'].ewm(span=macd_slow, adjust=False).mean()
    data['MACD_Signal'] = data['MACD'].ewm(span=macd_signal, adjust=False).mean()
    data['MACD_Hist'] = data['MACD'] - data['MACD_Signal']

    # Create Candlestick Chart with Bollinger Bands & MA
    fig_candlestick = go.Figure()
    fig_candlestick.add_trace(go.Candlestick(
        x=data.index,
        open=data['Open'], high=data['High'],
        low=data['Low'], close=data['Close'],
        name="Candlestick",
        increasing_line_color="green",
        decreasing_line_color="red"
    ))
    fig_candlestick.add_trace(go.Scatter(x=data.index, y=data['MA'], mode='lines', name=f"{ma_window}-day MA", line=dict(color="blue")))
    fig_candlestick.add_trace(go.Scatter(x=data.index, y=data['Upper_BB'], mode='lines', name="Upper BB", line=dict(color="purple", dash='dot')))
    fig_candlestick.add_trace(go.Scatter(x=data.index, y=data['Lower_BB'], mode='lines', name="Lower BB", line=dict(color="purple", dash='dot')))
    fig_candlestick.update_layout(title="📈 Stock Price with Bollinger Bands & MA", xaxis_rangeslider_visible=True, template="plotly_dark", height=500, width=900)

    # Create RSI Chart
    fig_rsi = go.Figure()
    fig_rsi.add_trace(go.Scatter(x=data.index, y=data['RSI'], mode='lines', name="RSI", line=dict(color="orange")))
    fig_rsi.add_trace(go.Scatter(x=data.index, y=[70]*len(data), mode='lines', name="Overbought (70)", line=dict(color="red", dash='dash')))
    fig_rsi.add_trace(go.Scatter(x=data.index, y=[30]*len(data), mode='lines', name="Oversold (30)", line=dict(color="green", dash='dash')))
    fig_rsi.update_layout(title="📊 Relative Strength Index (RSI)", xaxis_rangeslider_visible=False, template="plotly_dark", height=500, width=900)

    # Create MACD Chart
    fig_macd = go.Figure()
    fig_macd.add_trace(go.Scatter(x=data.index, y=data['MACD'], mode='lines', name="MACD", line=dict(color="blue")))
    fig_macd.add_trace(go.Scatter(x=data.index, y=data['MACD_Signal'], mode='lines', name="MACD Signal", line=dict(color="red")))
    fig_macd.add_trace(go.Bar(x=data.index, y=data['MACD_Hist'], name="MACD Histogram", marker_color="purple"))
    fig_macd.update_layout(title="📉 MACD Indicator", xaxis_rangeslider_visible=False, template="plotly_dark", height=500, width=900)

    # Display Charts One Below Another**
    st.subheader("📈 Stock Price with Bollinger Bands & Moving Averages")
    st.plotly_chart(fig_candlestick, use_container_width=True)  # Stock Chart

    st.subheader("📊 Relative Strength Index (RSI)")
    st.plotly_chart(fig_rsi, use_container_width=True)  # RSI Chart

    st.subheader("📉 MACD Indicator")
    st.plotly_chart(fig_macd, use_container_width=True)  # MACD Chart


    print(data.columns)

    return data
