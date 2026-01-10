"""
Test script for multi-source data provider.
Tests Yahoo Finance, Alpha Vantage, and Polygon.io fallback mechanism.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.data_sources import MarketDataProvider, DataSourceError
import os


def test_data_sources():
    """Test all configured data sources."""
    print("=" * 80)
    print("MARKET DATA PROVIDER - MULTI-SOURCE TEST")
    print("=" * 80)

    # Check which API keys are configured
    print("\n📋 Configuration Check:")
    print(f"   OpenAI API Key:      {'✓ Set' if os.getenv('OPENAI_API_KEY') else '✗ Not set'}")
    print(f"   Alpha Vantage Key:   {'✓ Set' if os.getenv('ALPHA_VANTAGE_API_KEY') else '✗ Not set (optional)'}")
    print(f"   Polygon.io Key:      {'✓ Set' if os.getenv('POLYGON_API_KEY') else '✗ Not set (optional)'}")

    print("\n" + "=" * 80)
    print("TESTING DATA PROVIDER")
    print("=" * 80)

    provider = MarketDataProvider()
    print(f"\nInitialized with {len(provider.sources)} data source(s):")
    for i, source in enumerate(provider.sources, 1):
        print(f"   {i}. {source.name}")

    # Test ticker
    ticker = "AAPL"
    print(f"\n🔍 Testing ticker: {ticker}")
    print("   Attempting to fetch quote data...")

    try:
        data = provider.get_quote(ticker)

        print("\n✅ SUCCESS! Data retrieved:")
        print("=" * 80)
        print(f"Symbol:         {data.get('symbol', ticker)}")
        print(f"Current Price:  ${data.get('currentPrice', 'N/A')}")
        print(f"Open:           ${data.get('open', 'N/A')}")
        print(f"High:           ${data.get('dayHigh', 'N/A')}")
        print(f"Low:            ${data.get('dayLow', 'N/A')}")
        print(f"Volume:         {data.get('volume', 'N/A'):,}" if isinstance(data.get('volume'), (int, float)) else f"Volume:         N/A")
        print("=" * 80)

        # Test historical data
        print("\n📊 Testing historical data fetch...")
        try:
            hist = provider.get_history(ticker, period="1mo")
            print(f"✅ Historical data retrieved: {len(hist)} days")
            print(f"   Date range: {hist.index[0].date()} to {hist.index[-1].date()}")
            print(f"   Latest close: ${hist['Close'].iloc[-1]:.2f}")

        except DataSourceError as e:
            print(f"⚠️  Historical data failed: {str(e)}")
            print("   (This is expected if Yahoo Finance is blocked)")

    except DataSourceError as e:
        print(f"\n❌ FAILED: {str(e)}")
        print("\n💡 Solutions:")
        print("   1. Wait 1-2 hours for Yahoo Finance rate limit to reset")
        print("   2. Use VPN to get a new IP address")
        print("   3. Configure Alpha Vantage or Polygon.io API keys:")
        print("      • Alpha Vantage: https://www.alphavantage.co/support/#api-key")
        print("      • Polygon.io: https://polygon.io/")
        print("   4. Run: ./setup_api_keys.sh")

    print("\n" + "=" * 80)
    print("RECOMMENDATIONS")
    print("=" * 80)

    if not os.getenv('ALPHA_VANTAGE_API_KEY') and not os.getenv('POLYGON_API_KEY'):
        print("""
⚠️  WARNING: No fallback data sources configured!

For production reliability, we recommend:

1. Alpha Vantage (FREE - 500 requests/day)
   → Best for: Technical indicators (RSI, MACD built-in)
   → Sign up: https://www.alphavantage.co/support/#api-key
   → Add to .env: ALPHA_VANTAGE_API_KEY=your_key_here

2. Polygon.io (FREE - 5 req/min, or $29/month unlimited)
   → Best for: High-quality real-time data
   → Sign up: https://polygon.io/
   → Add to .env: POLYGON_API_KEY=your_key_here

Run the setup script:
   ./setup_api_keys.sh

Or manually add to .env file:
   echo "ALPHA_VANTAGE_API_KEY=your_key" >> .env
        """)
    else:
        print("""
✅ You have fallback data sources configured!

The system will automatically try sources in this order:
   1. Yahoo Finance (free, primary)
   2. Alpha Vantage (if configured)
   3. Polygon.io (if configured)

This provides excellent reliability even if Yahoo Finance is blocked.
        """)

    print("=" * 80)


if __name__ == "__main__":
    test_data_sources()
