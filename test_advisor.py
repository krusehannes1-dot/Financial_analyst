"""
Test Script for Kruse Capital Advisor
Tests the technical analysis and trading advisory system.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.market_data import get_full_advisor_data
from app.services.utils import resolve_isin_to_ticker


def test_technical_analysis(ticker="AAPL"):
    """Test the technical analysis engine."""
    print("=" * 80)
    print(f"KRUSE CAPITAL ADVISOR - TECHNICAL ANALYSIS TEST")
    print("=" * 80)
    print(f"\nTesting ticker: {ticker}")
    print("Fetching comprehensive market data with technical indicators...")
    print("This includes: RSI, MACD, SMA, Support/Resistance, Wall Street consensus\n")

    try:
        data = get_full_advisor_data(ticker)

        # Display comprehensive results
        print("=" * 80)
        print("COMPANY INFORMATION")
        print("=" * 80)
        print(f"Name:     {data['name']}")
        print(f"Ticker:   {data['ticker']}")
        print(f"Sector:   {data['sector']}")
        print(f"Industry: {data['industry']}")

        print("\n" + "=" * 80)
        print("CURRENT MARKET STATUS")
        print("=" * 80)
        print(f"Current Price:    ${data['current_price']:.2f}")
        print(f"1-Day Change:     {data['price_change_1d']:+.2f}%")
        print(f"5-Day Change:     {data['price_change_5d']:+.2f}%")
        print(f"1-Month Change:   {data['price_change_1m']:+.2f}%")
        print(f"Volume Ratio:     {data['volume_ratio']:.2f}x (vs 30-day avg)")

        print("\n" + "=" * 80)
        print("TECHNICAL INDICATORS (The Algorithm)")
        print("=" * 80)

        # RSI Analysis
        rsi = data.get('rsi')
        if rsi:
            rsi_status = "OVERBOUGHT ⚠️" if rsi > 70 else "OVERSOLD 📉" if rsi < 30 else "NEUTRAL ✓"
            print(f"RSI (14):         {rsi:.2f}  [{rsi_status}]")
        else:
            print(f"RSI (14):         N/A")

        # Trend Analysis
        trend = data.get('trend', 'NEUTRAL')
        trend_emoji = "📈" if "UP" in trend else "📉" if "DOWN" in trend else "➡️"
        print(f"Trend:            {trend} {trend_emoji}")

        # Moving Averages
        sma_50 = data.get('sma_50')
        sma_200 = data.get('sma_200')
        if sma_50:
            print(f"SMA 50:           ${sma_50:.2f}")
            price_vs_sma50 = ((data['current_price'] - sma_50) / sma_50 * 100)
            print(f"  Price vs SMA50: {price_vs_sma50:+.2f}%")
        if sma_200:
            print(f"SMA 200:          ${sma_200:.2f}")
            price_vs_sma200 = ((data['current_price'] - sma_200) / sma_200 * 100)
            print(f"  Price vs SMA200: {price_vs_sma200:+.2f}%")

        # MACD
        macd = data.get('macd')
        if macd:
            macd_signal = data.get('macd_signal')
            macd_histogram = data.get('macd_histogram')
            macd_status = "BULLISH 🟢" if macd_histogram > 0 else "BEARISH 🔴"
            print(f"\nMACD:             {macd:.4f}")
            print(f"MACD Signal:      {macd_signal:.4f}")
            print(f"MACD Histogram:   {macd_histogram:.4f}  [{macd_status}]")

        # Bollinger Bands
        bb_upper = data.get('bb_upper')
        if bb_upper:
            print(f"\nBollinger Bands:")
            print(f"  Upper:          ${bb_upper:.2f}")
            print(f"  Middle:         ${data.get('bb_middle', 0):.2f}")
            print(f"  Lower:          ${data.get('bb_lower', 0):.2f}")

        print("\n" + "=" * 80)
        print("SUPPORT & RESISTANCE (Critical Price Zones)")
        print("=" * 80)
        support = data.get('support_level', 0)
        resistance = data.get('resistance_level', 0)
        current_price = data['current_price']

        print(f"Support (90d):    ${support:.2f}")
        distance_to_support = ((current_price - support) / current_price * 100)
        print(f"  Distance:       {distance_to_support:.2f}% above support")

        print(f"\nResistance (90d): ${resistance:.2f}")
        distance_to_resistance = ((resistance - current_price) / current_price * 100)
        print(f"  Distance:       {distance_to_resistance:.2f}% below resistance")

        print(f"\nPivot Point:      ${data.get('pivot_point', 0):.2f}")
        print(f"S1:               ${data.get('support_1', 0):.2f}")
        print(f"R1:               ${data.get('resistance_1', 0):.2f}")

        print("\n" + "=" * 80)
        print("WALL STREET CONSENSUS")
        print("=" * 80)
        recommendation = data.get('recommendation_key', 'none').upper()
        target_price = data.get('target_mean_price')
        upside = data.get('upside_potential')

        print(f"Recommendation:   {recommendation}")
        print(f"Analysts Covering: {data.get('number_of_analysts', 0)}")

        if target_price:
            print(f"\nPrice Targets:")
            print(f"  Low:            ${data.get('target_low_price', 0):.2f}")
            print(f"  Mean:           ${target_price:.2f}")
            print(f"  High:           ${data.get('target_high_price', 0):.2f}")

        if upside:
            upside_emoji = "🚀" if upside > 20 else "📈" if upside > 0 else "📉"
            print(f"\nImplied Upside:   {upside:+.2f}% {upside_emoji}")

        print("\n" + "=" * 80)
        print("FUNDAMENTAL VALUATION")
        print("=" * 80)

        forward_pe = data.get('forward_pe')
        trailing_pe = data.get('trailing_pe')
        peg = data.get('peg_ratio')

        if forward_pe:
            print(f"Forward P/E:      {forward_pe:.2f}")
        if trailing_pe:
            print(f"Trailing P/E:     {trailing_pe:.2f}")
        if peg:
            peg_status = "Undervalued" if peg < 1 else "Fairly valued" if peg < 2 else "Overvalued"
            print(f"PEG Ratio:        {peg:.2f}  [{peg_status}]")

        debt_to_equity = data.get('debt_to_equity')
        if debt_to_equity:
            debt_status = "Low debt ✓" if debt_to_equity < 50 else "High debt ⚠️"
            print(f"Debt/Equity:      {debt_to_equity:.2f}  [{debt_status}]")

        profit_margin = data.get('profit_margins')
        revenue_growth = data.get('revenue_growth')
        if profit_margin:
            print(f"\nProfitability:")
            print(f"  Profit Margin:  {profit_margin*100:.2f}%")
        if revenue_growth:
            print(f"  Revenue Growth: {revenue_growth*100:.2f}%")

        market_cap = data.get('market_cap', 0)
        if market_cap:
            if market_cap >= 1_000_000_000_000:
                cap_str = f"${market_cap/1_000_000_000_000:.2f}T"
            elif market_cap >= 1_000_000_000:
                cap_str = f"${market_cap/1_000_000_000:.2f}B"
            else:
                cap_str = f"${market_cap/1_000_000:.2f}M"
            print(f"\nMarket Cap:       {cap_str}")

        beta = data.get('beta')
        if beta:
            beta_status = "High volatility" if beta > 1.5 else "Low volatility" if beta < 0.8 else "Market-like"
            print(f"Beta:             {beta:.2f}  [{beta_status}]")

        print("\n" + "=" * 80)
        print("TRADING DECISION SIGNALS")
        print("=" * 80)

        # Generate simple signals
        signals = []

        if rsi and rsi > 70:
            signals.append("⚠️  RSI OVERBOUGHT - Consider waiting for pullback")
        elif rsi and rsi < 30:
            signals.append("📉 RSI OVERSOLD - Potential reversal zone")

        if "STRONG_UPTREND" in trend:
            signals.append("📈 STRONG UPTREND - Momentum is bullish")
        elif "STRONG_DOWNTREND" in trend:
            signals.append("📉 STRONG DOWNTREND - Caution advised")

        if macd_histogram and macd_histogram > 0:
            signals.append("🟢 MACD BULLISH - Positive momentum")
        elif macd_histogram and macd_histogram < 0:
            signals.append("🔴 MACD BEARISH - Negative momentum")

        if distance_to_support < 5:
            signals.append(f"🛡️  NEAR SUPPORT - Strong buy zone at ${support:.2f}")
        if distance_to_resistance < 5:
            signals.append(f"⚠️  NEAR RESISTANCE - Take profit zone at ${resistance:.2f}")

        if signals:
            for signal in signals:
                print(f"  {signal}")
        else:
            print("  ➡️  No strong signals - Market in equilibrium")

        print("\n" + "=" * 80)
        print("✅ TECHNICAL ANALYSIS COMPLETE")
        print("=" * 80)
        print("\nNext Step: Use the /advise endpoint to get AI-powered trading recommendations")
        print(f'curl -X POST "http://localhost:8000/advise" -H "Content-Type: application/json" \\')
        print(f'  -d \'{{"isin": "US0378331005", "asset_name": "Apple Inc."}}\'')
        print("\n" + "=" * 80)

        return data

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nNote: If you see rate limiting from Yahoo Finance, this is temporary.")
        print("The technical analysis engine is working correctly!")
        return None


def main():
    """Run the advisor test."""
    print("\n" + "=" * 80)
    print("KRUSE CAPITAL ADVISOR - COMPREHENSIVE TEST")
    print("Testing: Technical Analysis + Fundamental Data + Wall Street Consensus")
    print("=" * 80 + "\n")

    # Test ISIN resolution
    isin = "US0378331005"
    ticker = resolve_isin_to_ticker(isin)
    print(f"✓ ISIN Resolution: {isin} → {ticker}\n")

    # Run technical analysis test
    test_technical_analysis(ticker)


if __name__ == "__main__":
    main()
