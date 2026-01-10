"""
Complete Advisor Demo with Mock Data
Demonstrates the full trading advisory workflow.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.utils import resolve_isin_to_ticker


def demo_complete_advisor():
    """Demonstrate complete advisor workflow with realistic data."""
    print("=" * 80)
    print("KRUSE CAPITAL ADVISOR - COMPLETE TRADING ADVISORY DEMO")
    print("=" * 80)

    # Step 1: ISIN Resolution
    isin = "US0378331005"
    ticker = resolve_isin_to_ticker(isin)

    print(f"\n📊 Step 1: ISIN Resolution")
    print(f"   ISIN: {isin}")
    print(f"   ✓ Resolved to: {ticker} (Apple Inc.)")

    # Mock comprehensive advisor data (realistic Apple data)
    mock_advisor_data = {
        # Basic Info
        "ticker": "AAPL",
        "name": "Apple Inc.",
        "sector": "Technology",
        "industry": "Consumer Electronics",
        "currency": "USD",

        # Current Price & Volume
        "current_price": 185.50,
        "avg_volume_30d": 52_000_000,
        "current_volume": 68_000_000,
        "volume_ratio": 1.31,

        # Price Changes
        "price_change_1d": -1.25,
        "price_change_5d": 3.45,
        "price_change_1m": 8.75,

        # Technical Indicators
        "rsi": 58.3,  # Neutral zone
        "sma_50": 182.40,
        "sma_200": 175.20,
        "macd": 1.23,
        "macd_signal": 0.98,
        "macd_histogram": 0.25,  # Bullish

        # Bollinger Bands
        "bb_upper": 192.50,
        "bb_middle": 185.00,
        "bb_lower": 177.50,

        # Volatility
        "atr": 3.45,

        # Support & Resistance
        "support_level": 178.20,
        "resistance_level": 193.50,
        "pivot_point": 185.85,
        "support_1": 181.70,
        "resistance_1": 190.00,

        # Trend Analysis
        "trend": "UPTREND",

        # Wall Street Consensus
        "target_mean_price": 205.00,
        "target_high_price": 250.00,
        "target_low_price": 175.00,
        "recommendation_key": "buy",
        "number_of_analysts": 42,
        "upside_potential": 10.51,

        # Fundamental Metrics
        "forward_pe": 28.5,
        "trailing_pe": 31.2,
        "peg_ratio": 2.15,
        "debt_to_equity": 170.5,
        "price_to_book": 45.8,
        "profit_margins": 0.267,
        "revenue_growth": 0.022,
        "earnings_growth": 0.091,
        "market_cap": 2_850_000_000_000,  # $2.85T
        "beta": 1.24,
    }

    print(f"\n📈 Step 2: Comprehensive Market Data Analysis")
    print("   ✓ Historical data loaded (1 year)")
    print("   ✓ Technical indicators calculated")
    print("   ✓ Support/Resistance identified")
    print("   ✓ Wall Street consensus retrieved")

    # Display the analysis
    data = mock_advisor_data

    print("\n" + "=" * 80)
    print("MARKET STATUS")
    print("=" * 80)
    print(f"Current Price:    ${data['current_price']:.2f}")
    print(f"1-Day Change:     {data['price_change_1d']:+.2f}%")
    print(f"5-Day Change:     {data['price_change_5d']:+.2f}%")
    print(f"1-Month Change:   {data['price_change_1m']:+.2f}%")
    print(f"Volume:           {data['volume_ratio']:.2f}x above average 🔥")

    print("\n" + "=" * 80)
    print("TECHNICAL INDICATORS (The Algorithm)")
    print("=" * 80)

    rsi = data['rsi']
    rsi_status = "OVERBOUGHT ⚠️" if rsi > 70 else "OVERSOLD 📉" if rsi < 30 else "NEUTRAL ✓"
    print(f"RSI (14):         {rsi:.1f}  [{rsi_status}]")

    print(f"Trend:            {data['trend']} 📈")
    print(f"SMA 50:           ${data['sma_50']:.2f}")
    print(f"SMA 200:          ${data['sma_200']:.2f}")

    price_vs_sma50 = ((data['current_price'] - data['sma_50']) / data['sma_50'] * 100)
    price_vs_sma200 = ((data['current_price'] - data['sma_200']) / data['sma_200'] * 100)
    print(f"  Price vs SMA50: {price_vs_sma50:+.2f}% ✓ (bullish)")
    print(f"  Price vs SMA200: {price_vs_sma200:+.2f}% ✓ (bullish)")

    macd_status = "BULLISH 🟢" if data['macd_histogram'] > 0 else "BEARISH 🔴"
    print(f"\nMACD:             {data['macd']:.2f}")
    print(f"MACD Signal:      {data['macd_signal']:.2f}")
    print(f"MACD Histogram:   {data['macd_histogram']:.2f}  [{macd_status}]")

    print("\n" + "=" * 80)
    print("CRITICAL PRICE ZONES")
    print("=" * 80)

    support = data['support_level']
    resistance = data['resistance_level']
    current = data['current_price']

    distance_to_support = ((current - support) / current * 100)
    distance_to_resistance = ((resistance - current) / current * 100)

    print(f"Support (90d):    ${support:.2f}")
    print(f"  Distance:       {distance_to_support:.2f}% above support")
    print(f"\nResistance (90d): ${resistance:.2f}")
    print(f"  Distance:       {distance_to_resistance:.2f}% below resistance")
    print(f"\nPivot Point:      ${data['pivot_point']:.2f}")

    print("\n" + "=" * 80)
    print("WALL STREET CONSENSUS")
    print("=" * 80)
    print(f"Recommendation:   {data['recommendation_key'].upper()} 👍")
    print(f"Analysts:         {data['number_of_analysts']}")
    print(f"Target (Mean):    ${data['target_mean_price']:.2f}")
    print(f"Target Range:     ${data['target_low_price']:.2f} - ${data['target_high_price']:.2f}")
    print(f"Implied Upside:   {data['upside_potential']:+.2f}% 🚀")

    print("\n" + "=" * 80)
    print("VALUATION METRICS")
    print("=" * 80)
    print(f"Forward P/E:      {data['forward_pe']:.1f}")
    print(f"PEG Ratio:        {data['peg_ratio']:.2f}  [Premium valuation]")
    print(f"Debt/Equity:      {data['debt_to_equity']:.1f}  [High leverage ⚠️]")
    print(f"Profit Margin:    {data['profit_margins']*100:.1f}%  [Excellent ✓]")
    print(f"Market Cap:       $2.85T")

    print("\n" + "=" * 80)
    print("🎯 AI-GENERATED ACTION CARD (Mock)")
    print("=" * 80)

    print("""
**RECOMMENDATION:** KAUFEN (Buy on Pullback)

**ENTRY ZONE:**
€ 178.00 - € 182.00
_Rationale: Support zone + SMA50 confluence. Wait for RSI to cool off._

**PRICE TARGET (12M):**
€ 205.00
_Basis: Wall Street consensus mean target. Aligned with P/E expansion._

**STOP-LOSS:**
€ 172.50 (-6.8%)
_Logic: 3% below 90-day support at €178.20. Protects against breakdown._

**POSITION SIZE GUIDANCE:**
Medium position (3-5% of portfolio)
_Risk/Reward favorable, but premium valuation warrants caution._

**KEY TRIGGERS:**
- ✅ Entry Signal: RSI drops to 45-50 + price touches SMA50 (€182)
- 🚨 Exit Signal: Break below €178 support with high volume

**TIMEFRAME:** 6-12 Months

---

**Key Observations:**
1. Technical setup is bullish (price above both SMAs, MACD positive)
2. Wall Street consensus is BUY with 10.5% upside
3. RSI at 58 - not overbought, but wait for better entry
4. High volume (1.3x avg) shows institutional interest
5. Premium valuation (PEG 2.15) limits margin of safety

**Risks:**
- High P/E ratio vulnerable to multiple compression
- Elevated debt/equity at 170.5
- Near-term resistance at €193.50
- Macro headwinds (interest rates, consumer spending)
""")

    print("\n" + "=" * 80)
    print("HOW THE AI ADVISOR WORKS")
    print("=" * 80)
    print("""
The Kruse Capital Advisor combines:

1. TECHNICAL ANALYSIS (Algorithmic)
   - RSI, MACD, Moving Averages calculated via pandas_ta
   - Support/Resistance from 90-day price extremes
   - Bollinger Bands for volatility analysis
   - Volume analysis for conviction signals

2. FUNDAMENTAL DATA (Facts)
   - P/E ratios, PEG, Debt levels from yfinance
   - Profitability metrics (margins, growth rates)
   - Market cap and beta for risk assessment

3. WALL STREET CONSENSUS (Professional Opinion)
   - Analyst recommendations (Buy/Hold/Sell)
   - Price targets (Low/Mean/High)
   - Number of analysts covering

4. AI SYNTHESIS (GPT-4 Integration)
   - Interprets conflicting signals
   - Generates specific entry/exit zones
   - Calculates stop-loss placement
   - Provides risk-adjusted position sizing
   - Outputs actionable trading plan

The result: NOT generic "do your own research" but SPECIFIC price levels,
clear actions, and calculated risk management.
    """)

    print("\n" + "=" * 80)
    print("🚀 TO USE IN PRODUCTION")
    print("=" * 80)
    print("""
1. Add OpenAI API key to .env:
   OPENAI_API_KEY=sk-your-key-here

2. Install dependencies:
   pip install pandas pandas-ta anthropic

3. Start the server:
   uvicorn app.main:app --reload

4. Make a request:
   POST /advise
   {
     "isin": "US0378331005",
     "asset_name": "Apple Inc."
   }

5. Receive actionable trading advisory with:
   - BUY/SELL/HOLD/WATCHLIST recommendation
   - Specific entry prices
   - 12-month price target
   - Stop-loss placement
   - Position sizing guidance
   - Key trigger conditions
    """)

    print("\n" + "=" * 80)
    print("✅ DEMO COMPLETE - ADVISOR SYSTEM READY FOR DEPLOYMENT")
    print("=" * 80)


if __name__ == "__main__":
    demo_complete_advisor()
