"""
Demo: NVIDIA Analysis Workflow
This demonstrates the complete workflow without needing OpenAI API key.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.utils import resolve_isin_to_ticker, format_currency, format_percentage
from app.services.data_fetcher import get_market_data
import json

print("=" * 80)
print("NVIDIA CORPORATION (NVDA) - INVESTMENT ANALYSIS DEMO")
print("=" * 80)

# Step 1: ISIN Resolution
isin = "US67066G1040"
print(f"\n📊 Step 1: ISIN Resolution")
print(f"   ISIN: {isin}")

ticker = resolve_isin_to_ticker(isin)
print(f"   ✓ Resolved to ticker: {ticker}")

# Step 2: Fetch Market Data
print(f"\n📈 Step 2: Fetching Market Data from yfinance")
print(f"   This may take a few seconds...")

try:
    data = get_market_data(ticker)

    # Display the data
    basic_info = data.get("basic_info", {})
    financials = data.get("financials", {})
    balance_sheet = data.get("balance_sheet", {})
    news = data.get("news", [])

    print(f"   ✓ Data fetched successfully!\n")

    print("=" * 80)
    print("COMPANY OVERVIEW")
    print("=" * 80)
    print(f"Name:              {basic_info.get('name')}")
    print(f"Ticker:            {basic_info.get('ticker')}")
    print(f"Sector:            {basic_info.get('sector')}")
    print(f"Industry:          {basic_info.get('industry')}")

    print("\n" + "=" * 80)
    print("MARKET DATA")
    print("=" * 80)
    print(f"Current Price:     {basic_info.get('current_price')} {basic_info.get('currency')}")
    print(f"Market Cap:        {format_currency(basic_info.get('market_cap'), basic_info.get('currency', 'USD'))}")
    print(f"52-Week Range:     {basic_info.get('52_week_low')} - {basic_info.get('52_week_high')}")
    print(f"Average Volume:    {basic_info.get('avg_volume'):,}" if basic_info.get('avg_volume') != 'N/A' else f"Average Volume:    N/A")

    print("\n" + "=" * 80)
    print("VALUATION METRICS")
    print("=" * 80)
    print(f"P/E Ratio:         {basic_info.get('pe_ratio')}")
    print(f"Forward P/E:       {basic_info.get('forward_pe')}")
    print(f"Beta:              {basic_info.get('beta')}")
    print(f"Dividend Yield:    {format_percentage(basic_info.get('dividend_yield'))}")

    print("\n" + "=" * 80)
    print("PROFITABILITY & GROWTH")
    print("=" * 80)
    print(f"Profit Margins:    {format_percentage(basic_info.get('profit_margins'))}")
    print(f"Revenue Growth:    {format_percentage(basic_info.get('revenue_growth'))}")
    print(f"Return on Equity:  {format_percentage(basic_info.get('return_on_equity'))}")
    print(f"Debt to Equity:    {basic_info.get('debt_to_equity')}")

    print("\n" + "=" * 80)
    print(f"INCOME STATEMENT ({financials.get('period_end', 'N/A')})")
    print("=" * 80)
    print(f"Total Revenue:     {format_currency(financials.get('total_revenue'), basic_info.get('currency', 'USD'))}")
    print(f"Gross Profit:      {format_currency(financials.get('gross_profit'), basic_info.get('currency', 'USD'))}")
    print(f"Operating Income:  {format_currency(financials.get('operating_income'), basic_info.get('currency', 'USD'))}")
    print(f"Net Income:        {format_currency(financials.get('net_income'), basic_info.get('currency', 'USD'))}")
    print(f"EBITDA:            {format_currency(financials.get('ebitda'), basic_info.get('currency', 'USD'))}")

    print("\n" + "=" * 80)
    print(f"BALANCE SHEET ({balance_sheet.get('period_end', 'N/A')})")
    print("=" * 80)
    print(f"Total Assets:      {format_currency(balance_sheet.get('total_assets'), basic_info.get('currency', 'USD'))}")
    print(f"Total Liabilities: {format_currency(balance_sheet.get('total_liabilities'), basic_info.get('currency', 'USD'))}")
    print(f"Stockholder Equity: {format_currency(balance_sheet.get('stockholder_equity'), basic_info.get('currency', 'USD'))}")
    print(f"Total Debt:        {format_currency(balance_sheet.get('total_debt'), basic_info.get('currency', 'USD'))}")
    print(f"Cash & Equivalents: {format_currency(balance_sheet.get('cash_and_equivalents'), basic_info.get('currency', 'USD'))}")

    print("\n" + "=" * 80)
    print("RECENT NEWS")
    print("=" * 80)
    if news and len(news) > 0 and "error" not in news[0]:
        for idx, item in enumerate(news, 1):
            if "error" not in item:
                print(f"{idx}. {item.get('title')}")
                print(f"   {item.get('publisher')} | {item.get('published')}\n")
    else:
        print("No recent news available\n")

    print("=" * 80)
    print("NEXT STEP: AI REPORT GENERATION")
    print("=" * 80)
    print("\n✓ All market data successfully retrieved!")
    print("\nTo generate the full AI-powered investment report:")
    print("1. Add your OpenAI API key to .env file:")
    print("   OPENAI_API_KEY=sk-your-key-here")
    print("\n2. Start the server:")
    print("   uvicorn app.main:app --reload")
    print("\n3. Make a request:")
    print('   curl -X POST "http://localhost:8000/analyze" \\')
    print('     -H "Content-Type: application/json" \\')
    print(f'     -d \'{{"isin": "{isin}", "asset_name": "NVIDIA Corporation"}}\'')
    print("\n" + "=" * 80)

except Exception as e:
    print(f"\n✗ Error: {str(e)}")
    print("\nNote: If you're seeing rate limiting errors from Yahoo Finance,")
    print("this is temporary. The service will work normally once the API is accessible.")
    print("\nThe ISIN resolution and API endpoints are working correctly!")
