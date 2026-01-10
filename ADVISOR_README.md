# Kruse Capital Advisor - Trading Advisory Extension

## New Feature: Actionable Trading Advice

The Advisor extends the base Analyst with **quantitative trading recommendations** based on technical analysis, fundamentals, and AI synthesis.

## What's New

### 🎯 `/advise` Endpoint - The Trading Advisory

Unlike the `/analyze` endpoint which provides general investment research, `/advise` gives you:

- **Specific BUY/SELL/HOLD/WATCHLIST** recommendations
- **Entry zones** with exact price ranges
- **Price targets** (12-month projections)
- **Stop-loss placement** (calculated risk management)
- **Position sizing guidance**
- **Trigger conditions** (when to enter/exit)

### 📊 Technical Analysis Engine

Powered by `pandas_ta`, the advisor calculates:

#### Momentum Indicators
- **RSI (14)**: Identifies overbought (>70) and oversold (<30) conditions
- **MACD**: Trend-following momentum indicator
  - MACD Line vs Signal Line crossovers
  - Histogram for momentum strength

#### Trend Indicators
- **SMA 50 & 200**: Moving average trends
  - Golden Cross (bullish) / Death Cross (bearish) detection
  - Price position relative to key averages

#### Volatility Indicators
- **Bollinger Bands**: Price volatility and extreme zones
- **ATR (Average True Range)**: Volatility measurement

#### Support & Resistance
- **90-day extremes**: Key support and resistance levels
- **Pivot Points**: Mathematical support/resistance calculation
- **Price zones**: Critical levels for entry/exit decisions

### 📈 Wall Street Consensus Integration

- Analyst recommendations (Buy/Hold/Sell aggregate)
- Price targets (Low/Mean/High from sell-side analysts)
- Upside potential calculations
- Number of analysts covering

### 🧠 AI-Powered Decision Synthesis

The GPT-4 advisor:
- Interprets conflicting signals (e.g., bullish technicals vs overvaluation)
- Applies risk management rules (e.g., no buy when RSI > 70)
- Calculates optimal entry zones using support levels
- Places stop-losses 3-5% below support
- Generates actionable trading plans with specific prices

## Architecture

```
/advise Request Flow:
1. ISIN → Ticker Resolution (utils.py)
2. Historical Data Fetch (yfinance - 1 year)
3. Technical Calculation (market_data.py + pandas_ta)
   ├─ RSI, MACD, SMA calculations
   ├─ Support/Resistance detection
   └─ Bollinger Bands, ATR
4. Fundamental Metrics (yfinance info)
   ├─ P/E, PEG, Debt/Equity
   └─ Growth rates, margins
5. Wall Street Data (yfinance info)
   ├─ Analyst recommendations
   └─ Price targets
6. AI Synthesis (llm_advisor.py + GPT-4)
   ├─ Interpret all data
   ├─ Apply trading rules
   └─ Generate Action Card
7. Return Advisory Report (Markdown)
```

## New Files

### [app/services/market_data.py](app/services/market_data.py)
Complete technical analysis engine:
- `get_full_advisor_data(ticker)`: Fetches and calculates all indicators
- Returns comprehensive dict with 40+ data points

Key functions:
```python
# Calculate RSI
hist['RSI'] = ta.rsi(hist['Close'], length=14)

# Calculate Moving Averages
hist['SMA_50'] = ta.sma(hist['Close'], length=50)
hist['SMA_200'] = ta.sma(hist['Close'], length=200)

# MACD calculation
macd = ta.macd(hist['Close'])

# Support/Resistance (90-day extremes)
support_level = recent_90d['Low'].min()
resistance_level = recent_90d['High'].max()
```

### [app/services/llm_advisor.py](app/services/llm_advisor.py)
AI-powered advisory report generator:
- `generate_advice_report(ticker, data)`: Creates actionable trading advisory
- System prompt: "Chief Investment Advisor" persona
- Enforces specific output format with Action Card

Critical AI rules enforced:
```python
"If RSI > 70, NEVER recommend immediate market buy"
"Stop-loss must be 3-5% below support"
"If data conflicts, explain divergence"
```

## Example: `/advise` Response

```json
{
  "success": true,
  "ticker": "AAPL",
  "isin": "US0378331005",
  "advisory_report": "# Trading Advisory: Apple Inc. (AAPL)\n\n...",
  "technical_data": {
    "rsi": 58.3,
    "trend": "UPTREND",
    "support_level": 178.20,
    "resistance_level": 193.50,
    "current_price": 185.50,
    "target_price": 205.00,
    "recommendation": "buy"
  },
  "metadata": {
    "asset_name": "Apple Inc.",
    "sector": "Technology",
    "data_timestamp": "2026-01-10T...",
    "analyst_count": 42
  }
}
```

### Action Card (inside `advisory_report`):

```markdown
## 🎯 ADVISOR ACTION CARD

**RECOMMENDATION:** KAUFEN (Buy on Pullback)

**ENTRY ZONE:**
€ 178.00 - € 182.00
_Rationale: Support zone + SMA50 confluence. RSI neutral._

**PRICE TARGET (12M):**
€ 205.00
_Basis: Wall Street consensus mean. PE expansion scenario._

**STOP-LOSS:**
€ 172.50 (-6.8%)
_Logic: 3% below 90-day support at €178.20._

**POSITION SIZE GUIDANCE:**
Medium position (3-5% of portfolio)

**KEY TRIGGERS:**
- ✅ Entry: RSI 45-50 + price at SMA50
- 🚨 Exit: Break below €178 on volume

**TIMEFRAME:** 6-12 Months
```

## Usage Examples

### cURL
```bash
curl -X POST "http://localhost:8000/advise" \
  -H "Content-Type: application/json" \
  -d '{
    "isin": "US0378331005",
    "asset_name": "Apple Inc."
  }'
```

### Python
```python
import requests

response = requests.post(
    "http://localhost:8000/advise",
    json={"isin": "US0378331005", "asset_name": "Apple Inc."}
)

data = response.json()
print(data["advisory_report"])  # Full markdown advisory
print(data["technical_data"])    # Key indicators
```

### JavaScript
```javascript
fetch('http://localhost:8000/advise', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    isin: 'US0378331005',
    asset_name: 'Apple Inc.'
  })
})
.then(res => res.json())
.then(data => {
  console.log(data.advisory_report);
  console.log('RSI:', data.technical_data.rsi);
  console.log('Recommendation:', data.technical_data.recommendation);
});
```

## Comparison: `/analyze` vs `/advise`

| Feature | `/analyze` | `/advise` |
|---------|-----------|----------|
| **Purpose** | General investment research | Actionable trading plan |
| **Output** | Investment thesis | BUY/SELL/HOLD + prices |
| **Technical Analysis** | ❌ | ✅ (RSI, MACD, S/R) |
| **Entry Zones** | ❌ | ✅ Specific prices |
| **Stop-Loss** | ❌ | ✅ Calculated |
| **Timeframe** | Long-term | 6-12 months |
| **Risk Management** | General | Specific (% stops) |
| **Use Case** | Due diligence | Trade execution |

## Trading Rules Implemented

The advisor follows strict quantitative rules:

1. **RSI Rules**:
   - RSI > 70: Wait for pullback, no immediate buy
   - RSI < 30: Check for "falling knife" in downtrend
   - RSI 40-60: Neutral zone, use other indicators

2. **Trend Rules**:
   - STRONG_UPTREND: Price > SMA50 > SMA200
   - UPTREND: SMA50 > SMA200
   - Downtrends: Caution, require stronger confirmation

3. **Support/Resistance Rules**:
   - Entry zones: Near support levels
   - Stop-loss: 3-5% below support
   - Resistance: Take-profit zones

4. **Volume Rules**:
   - Volume ratio > 1.5x: Strong conviction
   - Volume ratio < 0.8x: Weak signal

5. **Valuation Rules**:
   - PEG < 1: Undervalued
   - PEG 1-2: Fair value
   - PEG > 2: Overvalued (reduce position size)

## Installation (Additional Dependencies)

```bash
pip install pandas pandas-ta anthropic
```

Update `.env`:
```
OPENAI_API_KEY=sk-your-key-here
```

## Testing

Run the demo:
```bash
python3 demo_advisor_complete.py
```

This shows the full workflow with mock data.

## Configuration

### Customizing Technical Indicators

Edit [app/services/market_data.py](app/services/market_data.py:30):

```python
# Change RSI period
hist['RSI'] = ta.rsi(hist['Close'], length=14)  # Default: 14

# Change SMA periods
hist['SMA_50'] = ta.sma(hist['Close'], length=50)  # Default: 50, 200

# Change support/resistance lookback
recent_90d = hist.tail(90)  # Default: 90 days
```

### Customizing AI Behavior

Edit [app/services/llm_advisor.py](app/services/llm_advisor.py:15):

```python
# Modify system prompt
ADVISOR_SYSTEM_PROMPT = """
Your custom instructions here...
"""

# Adjust temperature (0.0 = deterministic, 1.0 = creative)
temperature=0.5  # Default: 0.5
```

## Roadmap

- [ ] Add more technical indicators (Ichimoku, Fibonacci)
- [ ] Sentiment analysis from news headlines
- [ ] Multi-timeframe analysis (daily, weekly, monthly)
- [ ] Backtesting framework
- [ ] Portfolio-level recommendations
- [ ] Real-time price alerts
- [ ] Options strategy recommendations

## License

Proprietary - Kruse Capital

## Support

For questions or feature requests, contact the development team.
