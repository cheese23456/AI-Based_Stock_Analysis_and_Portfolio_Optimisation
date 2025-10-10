# investment_signal.py
def get_investment_signal(ma, close_price, rsi, macd, lower_band, upper_band):
    """
    Simple rule-based decision:
      - RSI < 30 => Buy, RSI > 70 => Sell
      - MACD > 0 bullish, < 0 bearish
      - Price vs MA trend confirmation
      - Price vs Bollinger Bands for extremes
    Returns: (signal: 'Buy'|'Hold'|'Sell', reason: str)
    """
    reasons = []
    score = 0

    # RSI
    if rsi < 30:
        score += 2; reasons.append("RSI indicates oversold (<30)")
    elif rsi > 70:
        score -= 2; reasons.append("RSI indicates overbought (>70)")
    else:
        reasons.append("RSI is neutral (30–70)")

    # MACD
    if macd > 0:
        score += 1; reasons.append("MACD shows bullish momentum (>0)")
    else:
        score -= 1; reasons.append("MACD shows bearish momentum (<0)")

    # Trend vs MA
    if close_price > ma:
        score += 1; reasons.append("Price above MA (uptrend)")
    else:
        score -= 1; reasons.append("Price below MA (downtrend)")

    # Bollinger extremes
    if close_price < lower_band:
        score += 1; reasons.append("Price below lower Bollinger Band (potential rebound)")
    elif close_price > upper_band:
        score -= 1; reasons.append("Price above upper Bollinger Band (potential pullback)")

    if score >= 2:
        return "Buy", "; ".join(reasons)
    elif score <= -2:
        return "Sell", "; ".join(reasons)
    else:
        return "Hold", "; ".join(reasons)
