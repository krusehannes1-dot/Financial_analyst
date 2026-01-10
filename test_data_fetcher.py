"""
Test script for the data fetcher module.
Run this to verify that yfinance is working correctly before integrating with AI.
"""
import sys
from pathlib import Path

# Add the app directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.data_fetcher import get_market_data
from app.services.utils import resolve_isin_to_ticker, format_currency, format_percentage
import json


def test_isin_resolution():
    """Test ISIN to ticker resolution."""
    print("=" * 60)
    print("Testing ISIN Resolution")
    print("=" * 60)

    test_isins = [
        ("US0378331005", "Apple"),
        ("US5949181045", "Microsoft"),
        ("US88160R1014", "Tesla"),
    ]

    for isin, name in test_isins:
        ticker = resolve_isin_to_ticker(isin)
        status = "✓" if ticker else "✗"
        print(f"{status} {name:12} | ISIN: {isin} -> Ticker: {ticker or 'NOT FOUND'}")

    print()


def test_data_fetcher(ticker="AAPL"):
    """Test market data fetching."""
    print("=" * 60)
    print(f"Testing Data Fetcher for {ticker}")
    print("=" * 60)

    try:
        data = get_market_data(ticker)

        # Display basic info
        print("\n--- BASIC INFO ---")
        basic_info = data.get("basic_info", {})
        print(f"Name:            {basic_info.get('name')}")
        print(f"Ticker:          {basic_info.get('ticker')}")
        print(f"Sector:          {basic_info.get('sector')}")
        print(f"Industry:        {basic_info.get('industry')}")
        print(f"Current Price:   {basic_info.get('current_price')} {basic_info.get('currency')}")
        print(f"Market Cap:      {format_currency(basic_info.get('market_cap'))}")
        print(f"P/E Ratio:       {basic_info.get('pe_ratio')}")
        print(f"Forward P/E:     {basic_info.get('forward_pe')}")
        print(f"Dividend Yield:  {format_percentage(basic_info.get('dividend_yield'))}")
        print(f"Beta:            {basic_info.get('beta')}")

        # Display financials
        print("\n--- FINANCIALS ---")
        financials = data.get("financials", {})
        print(f"Period:          {financials.get('period_end')}")
        print(f"Total Revenue:   {format_currency(financials.get('total_revenue'))}")
        print(f"Gross Profit:    {format_currency(financials.get('gross_profit'))}")
        print(f"Operating Income: {format_currency(financials.get('operating_income'))}")
        print(f"Net Income:      {format_currency(financials.get('net_income'))}")
        print(f"EBITDA:          {format_currency(financials.get('ebitda'))}")

        # Display balance sheet
        print("\n--- BALANCE SHEET ---")
        balance_sheet = data.get("balance_sheet", {})
        print(f"Period:          {balance_sheet.get('period_end')}")
        print(f"Total Assets:    {format_currency(balance_sheet.get('total_assets'))}")
        print(f"Total Liabilities: {format_currency(balance_sheet.get('total_liabilities'))}")
        print(f"Equity:          {format_currency(balance_sheet.get('stockholder_equity'))}")
        print(f"Total Debt:      {format_currency(balance_sheet.get('total_debt'))}")
        print(f"Cash:            {format_currency(balance_sheet.get('cash_and_equivalents'))}")

        # Display news
        print("\n--- RECENT NEWS ---")
        news = data.get("news", [])
        if news:
            for idx, item in enumerate(news, 1):
                if "error" not in item:
                    print(f"{idx}. {item.get('title')}")
                    print(f"   Publisher: {item.get('publisher')} | {item.get('published')}")
        else:
            print("No news available")

        print("\n" + "=" * 60)
        print("✓ Data fetcher test completed successfully!")
        print("=" * 60)

        return data

    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        return None


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("DASHBOARD ANALYST - DATA FETCHER TEST")
    print("=" * 60 + "\n")

    # Test ISIN resolution
    test_isin_resolution()

    # Test data fetching
    print("Fetching data from yfinance...")
    print("This may take a few seconds...\n")

    data = test_data_fetcher("AAPL")

    if data:
        print("\n✓ All tests passed!")
        print("\nNext steps:")
        print("1. Add your OpenAI API key to the .env file")
        print("2. Run: uvicorn app.main:app --reload")
        print("3. Visit: http://localhost:8000/docs")
    else:
        print("\n✗ Tests failed. Please check your internet connection and try again.")


if __name__ == "__main__":
    main()
