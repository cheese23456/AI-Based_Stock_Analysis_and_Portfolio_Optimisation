# AI‑Based Stock Analysis & Portfolio Optimisation App

A Streamlit app that fetches market data, computes technical indicators (MA, RSI, MACD, Bollinger Bands), generates short AI insights, and produces a clear **Buy / Hold / Sell** signal per ticker. It can also run a simple **portfolio optimisation** over selected assets.

> **Demo:** If you deployed this on Hugging Face Spaces, open your Space URL:  
> `https://huggingface.co/spaces/<your-username>/<your-space-name>`  
> Replace the placeholders with your actual Space path.


## ✨ What you can do

- Enter 1..N tickers (e.g. `TSLA, AAPL` or `RELIANCE.NS, TCS.NS`)
- Choose date range and indicator windows and risk tolerance
- See charts + indicator values
- Read **AI one‑line insights** for MA/BB/RSI/MACD (optional; requires OpenAI key)
- Get a **color‑coded investment signal** (Buy / Hold / Sell) with reasons
- Optimise a simple **equal‑risk / target‑risk** allocation across your selection

> **Disclaimer:** This app is for **educational** use only. **Not** financial advice. Markets are risky; do your own research.


## 🧱 Project structure

```
.
├── app.py                          # Streamlit UI
├── data_loader.py                  # Robust price downloader using yfinance API
├── indicators.py                   # Indicator calculations and plots using Plotly
├── ai_insights.py                  # get_ai_insight() wrapper for OpenAI one‑liners
├── investment_signal.py            # get_investment_signal() – rule‑based Buy/Hold/Sell
├── portfolio_optimiser.py          # optimise weights from closing price data
└── requirements.txt                # dependencies (see variants below)
```


## 🛠️ Local setup

### 1) Create & activate a virtual environment
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 2) Install dependencies

**If your Python is 3.11+ (Windows/macOS/Linux):**
```txt
# requirements.txt
streamlit
yfinance
pandas
numpy==1.23.5
scipy
plotly
openai
```

Then install:
```bash
pip install -r requirements.txt
```

### 3) (Optional) Add your OpenAI API key
- **Env var** (works everywhere):
  ```bash
  # Windows (PowerShell)
  setx OPENAI_API_KEY "sk-..."
  # macOS/Linux (bash/zsh)
  export OPENAI_API_KEY="sk-..."
  ```
- **Streamlit secrets** (local): create `.streamlit/secrets.toml`
  ```toml
  OPENAI_API_KEY = "sk-..."
  ```

> Without a key, the app still runs – it just skips AI text.

### 4) Run the app
```bash
python -m streamlit run app.py
```
Then open the local URL (usually http://localhost:8501).


## 🚀 Hugging Face Spaces (demo & reproduce)

1. Create a new **Space → SDK: Streamlit**.
2. Upload your project files and **requirements.txt**.
3. For Spaces’ default **Python 3.10** image, use this `requirements.txt` (pinned to stable builds):
   ```txt
    streamlit
    yfinance
    pandas
    numpy==1.23.5
    scipy
    plotly
    openai
   ```
4. Set your `OPENAI_API_KEY` in **Settings → Variables & secrets** (optional).
5. Click **Restart** / **Rebuild**. Your app will be live at:  
   `https://huggingface.co/spaces/<your-username>/<your-space-name>`


## 📈 Indicators & Signal

**Indicators:**
- **MA** – Simple moving average (window configurable)
- **RSI** – Momentum (14 default)
- **MACD** – Trend / momentum (12, 26, 9 default)
- **Bollinger Bands** – Volatility bands (20, 2 default)
- **Risk Tolerance** – User Risk Tolerance between (0, 1)

**Signal (rule‑based):**
- Points for RSI (<30 oversold → +2; >70 overbought → −2)
- Points for MACD (>0 bullish → +1; <0 bearish → −1)
- Points for Trend (Close vs MA: above → +1; below → −1)
- Points for Bollinger extremes (below lower band → +1; above upper → −1)
- Total ≥ +2 → **Buy**; ≤ −2 → **Sell**; else **Hold**

> This is a transparent heuristic. Improve realism by adding **regime filters**, **confirmations**, **ATR‑based risk mgmt**, and a **walk‑forward backtest**.


## 🧪 Reproducibility checklist

- Use the pinned **requirements.txt** above.
- Fix a random seed where applicable (optimiser, if stochastic).
- Record the exact tickers and date range in your test.
- Export the final results (weights/metrics) with a timestamp for audit.


## 🩹 Troubleshooting

- **`streamlit: command not found` (Windows)**  
  Activate your venv and run via module:
  ```bash
  .venv\Scripts\activate
  python -m streamlit run app.py
  ```

- **OpenAI key not found**  
  Set `OPENAI_API_KEY` as an env var or in `.streamlit/secrets.toml`. The app handles missing keys gracefully.


## 🔐 Security & data usage

- Do **not** commit secrets (API keys). Use environment variables or platform secrets.
- This project fetches public market data for research and demo purposes only.

## 📜 License

MIT — free to use for learning and personal projects. If you build a commercial product, make sure your data sources comply with their respective terms.
