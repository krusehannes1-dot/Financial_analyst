"""
Mock Demo: NVIDIA Analysis with Sample Data
Demonstrates the complete workflow with mock data.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.utils import resolve_isin_to_ticker, format_currency, format_percentage

print("=" * 80)
print("NVIDIA CORPORATION (NVDA) - INVESTMENT ANALYSIS DEMO")
print("Using Mock Data (Yahoo Finance is rate-limited)")
print("=" * 80)

# Step 1: ISIN Resolution
isin = "US67066G1040"
print(f"\n📊 Step 1: ISIN Resolution")
print(f"   ISIN: {isin}")

ticker = resolve_isin_to_ticker(isin)
print(f"   ✓ Resolved to ticker: {ticker}")

# Step 2: Mock Market Data (realistic NVIDIA data)
print(f"\n📈 Step 2: Market Data (Mock)")

mock_data = {
    "basic_info": {
        "ticker": "NVDA",
        "name": "NVIDIA Corporation",
        "sector": "Technology",
        "industry": "Semiconductors",
        "current_price": 140.15,
        "currency": "USD",
        "market_cap": 3450000000000,  # $3.45T
        "pe_ratio": 52.8,
        "forward_pe": 28.5,
        "dividend_yield": 0.0003,
        "beta": 1.68,
        "52_week_high": 152.89,
        "52_week_low": 39.23,
        "avg_volume": 312500000,
        "profit_margins": 0.556,
        "revenue_growth": 1.22,
        "debt_to_equity": 18.52,
        "return_on_equity": 1.236,
    },
    "financials": {
        "period_end": "2024-01-28",
        "total_revenue": 60922000000,
        "gross_profit": 45347000000,
        "operating_income": 32967000000,
        "net_income": 29760000000,
        "ebitda": 35678000000,
    },
    "balance_sheet": {
        "period_end": "2024-01-28",
        "total_assets": 65728000000,
        "total_liabilities": 28426000000,
        "stockholder_equity": 42315000000,
        "total_debt": 8459000000,
        "cash_and_equivalents": 7280000000,
    },
    "news": [
        {
            "title": "NVIDIA Announces New AI Chip Architecture",
            "publisher": "Reuters",
            "published": "2026-01-09 14:30"
        },
        {
            "title": "Data Center Revenue Surges 217% Year-Over-Year",
            "publisher": "Bloomberg",
            "published": "2026-01-08 09:15"
        },
        {
            "title": "AI Demand Drives Record Quarterly Results",
            "publisher": "CNBC",
            "published": "2026-01-07 16:45"
        }
    ]
}

basic_info = mock_data["basic_info"]
financials = mock_data["financials"]
balance_sheet = mock_data["balance_sheet"]
news = mock_data["news"]

print(f"   ✓ Data loaded successfully!\n")

print("=" * 80)
print("COMPANY OVERVIEW")
print("=" * 80)
print(f"Name:              {basic_info['name']}")
print(f"Ticker:            {basic_info['ticker']}")
print(f"Sector:            {basic_info['sector']}")
print(f"Industry:          {basic_info['industry']}")

print("\n" + "=" * 80)
print("MARKET DATA")
print("=" * 80)
print(f"Current Price:     ${basic_info['current_price']:.2f}")
print(f"Market Cap:        {format_currency(basic_info['market_cap'], 'USD')}")
print(f"52-Week Range:     ${basic_info['52_week_low']:.2f} - ${basic_info['52_week_high']:.2f}")
print(f"Average Volume:    {basic_info['avg_volume']:,}")

print("\n" + "=" * 80)
print("VALUATION METRICS")
print("=" * 80)
print(f"P/E Ratio:         {basic_info['pe_ratio']:.1f}")
print(f"Forward P/E:       {basic_info['forward_pe']:.1f}")
print(f"Beta:              {basic_info['beta']:.2f}")
print(f"Dividend Yield:    {format_percentage(basic_info['dividend_yield'])}")

print("\n" + "=" * 80)
print("PROFITABILITY & GROWTH")
print("=" * 80)
print(f"Profit Margins:    {format_percentage(basic_info['profit_margins'])}")
print(f"Revenue Growth:    {format_percentage(basic_info['revenue_growth'])}")
print(f"Return on Equity:  {format_percentage(basic_info['return_on_equity'])}")
print(f"Debt to Equity:    {basic_info['debt_to_equity']:.2f}")

print("\n" + "=" * 80)
print(f"INCOME STATEMENT ({financials['period_end']})")
print("=" * 80)
print(f"Total Revenue:     {format_currency(financials['total_revenue'], 'USD')}")
print(f"Gross Profit:      {format_currency(financials['gross_profit'], 'USD')}")
print(f"Operating Income:  {format_currency(financials['operating_income'], 'USD')}")
print(f"Net Income:        {format_currency(financials['net_income'], 'USD')}")
print(f"EBITDA:            {format_currency(financials['ebitda'], 'USD')}")

# Calculate margins
gross_margin = (financials['gross_profit'] / financials['total_revenue']) * 100
operating_margin = (financials['operating_income'] / financials['total_revenue']) * 100
net_margin = (financials['net_income'] / financials['total_revenue']) * 100

print(f"\nMargins:")
print(f"  Gross Margin:    {gross_margin:.1f}%")
print(f"  Operating Margin: {operating_margin:.1f}%")
print(f"  Net Margin:      {net_margin:.1f}%")

print("\n" + "=" * 80)
print(f"BALANCE SHEET ({balance_sheet['period_end']})")
print("=" * 80)
print(f"Total Assets:      {format_currency(balance_sheet['total_assets'], 'USD')}")
print(f"Total Liabilities: {format_currency(balance_sheet['total_liabilities'], 'USD')}")
print(f"Stockholder Equity: {format_currency(balance_sheet['stockholder_equity'], 'USD')}")
print(f"Total Debt:        {format_currency(balance_sheet['total_debt'], 'USD')}")
print(f"Cash & Equivalents: {format_currency(balance_sheet['cash_and_equivalents'], 'USD')}")

# Calculate ratios
current_ratio = (balance_sheet['total_assets'] - balance_sheet['total_liabilities']) / balance_sheet['total_liabilities'] if balance_sheet['total_liabilities'] > 0 else 0
debt_to_assets = (balance_sheet['total_debt'] / balance_sheet['total_assets']) * 100 if balance_sheet['total_assets'] > 0 else 0

print(f"\nFinancial Ratios:")
print(f"  Debt to Assets:  {debt_to_assets:.1f}%")
print(f"  Equity Ratio:    {(balance_sheet['stockholder_equity'] / balance_sheet['total_assets'] * 100):.1f}%")

print("\n" + "=" * 80)
print("RECENT NEWS & CATALYSTS")
print("=" * 80)
for idx, item in enumerate(news, 1):
    print(f"{idx}. {item['title']}")
    print(f"   {item['publisher']} | {item['published']}\n")

print("=" * 80)
print("INVESTMENT ANALYSIS SUMMARY")
print("=" * 80)
print("\n🔍 Key Observations:")
print(f"   • Market leader in AI/GPU computing with ${format_currency(basic_info['market_cap'], 'USD')} market cap")
print(f"   • Exceptional profitability: {net_margin:.1f}% net margin")
print(f"   • Strong revenue growth: {format_percentage(basic_info['revenue_growth'])}")
print(f"   • Premium valuation: {basic_info['pe_ratio']:.1f}x P/E ratio")
print(f"   • Healthy balance sheet with low debt: {debt_to_assets:.1f}% debt-to-assets")

print("\n💡 Bull Case:")
print("   • Dominant position in AI chip market")
print("   • Explosive data center growth (217% YoY)")
print("   • Strong competitive moat in GPU technology")
print("   • Expanding into new markets (automotive, edge AI)")

print("\n⚠️  Bear Case:")
print("   • Very high P/E ratio suggests premium pricing")
print("   • Competition from AMD, Intel, and custom AI chips")
print("   • Potential regulatory scrutiny in China")
print("   • Cyclical semiconductor industry risks")

print("\n" + "=" * 80)
print("AI-POWERED REPORT GENERATION")
print("=" * 80)
print("\n📝 With an OpenAI API key, the system would generate a comprehensive")
print("   investment report including:")
print("   • Executive Summary")
print("   • Detailed Fundamental Analysis")
print("   • Comprehensive Bull/Bear Case")
print("   • News Impact Analysis")
print("   • Investment Recommendation")

print("\n🚀 To generate the full AI report:")
print("   1. Add OpenAI API key to .env:")
print("      OPENAI_API_KEY=sk-your-key-here")
print("\n   2. Start the server:")
print("      uvicorn app.main:app --reload")
print("\n   3. Make API request:")
print(f'      POST /analyze')
print(f'      {{ "isin": "{isin}", "asset_name": "NVIDIA Corporation" }}')

print("\n" + "=" * 80)
print("✅ DEMO COMPLETE - NVIDIA ANALYSIS SYSTEM READY")
print("=" * 80)
