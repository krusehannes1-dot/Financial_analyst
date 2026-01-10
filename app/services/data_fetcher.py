"""
Data Fetcher Service
Retrieves financial data from yfinance and structures it for analysis.
"""
import yfinance as yf
from typing import Dict, Any, Optional, List
from datetime import datetime
import time
import random

# Configure yfinance with browser-like headers to avoid blocking
import requests
yf.utils.get_json = lambda url, proxy=None, headers=None: requests.get(
    url,
    proxies=proxy,
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://finance.yahoo.com/'
    }
).json()


def get_market_data(ticker: str) -> Dict[str, Any]:
    """
    Fetch comprehensive market data for a given ticker.

    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'MSFT')

    Returns:
        Dictionary containing structured market data including:
        - Basic info (price, market cap, PE ratio, sector)
        - Financial statements (income statement, balance sheet)
        - Recent news headlines
    """
    try:
        # Add random delay to avoid rate limiting
        time.sleep(random.uniform(0.5, 1.5))

        stock = yf.Ticker(ticker)

        # Get basic info
        info = stock.info

        # Extract key metrics
        basic_data = {
            "ticker": ticker,
            "name": info.get("longName", "N/A"),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "current_price": info.get("currentPrice", info.get("regularMarketPrice", "N/A")),
            "currency": info.get("currency", "USD"),
            "market_cap": info.get("marketCap", "N/A"),
            "pe_ratio": info.get("trailingPE", "N/A"),
            "forward_pe": info.get("forwardPE", "N/A"),
            "dividend_yield": info.get("dividendYield", "N/A"),
            "beta": info.get("beta", "N/A"),
            "52_week_high": info.get("fiftyTwoWeekHigh", "N/A"),
            "52_week_low": info.get("fiftyTwoWeekLow", "N/A"),
            "avg_volume": info.get("averageVolume", "N/A"),
            "profit_margins": info.get("profitMargins", "N/A"),
            "revenue_growth": info.get("revenueGrowth", "N/A"),
            "debt_to_equity": info.get("debtToEquity", "N/A"),
            "return_on_equity": info.get("returnOnEquity", "N/A"),
        }

        # Get financial statements
        financials_data = _get_financials(stock)

        # Get balance sheet data
        balance_sheet_data = _get_balance_sheet(stock)

        # Get recent news
        news_data = _get_news(stock)

        # Combine all data
        return {
            "basic_info": basic_data,
            "financials": financials_data,
            "balance_sheet": balance_sheet_data,
            "news": news_data,
            "fetched_at": datetime.now().isoformat()
        }

    except Exception as e:
        raise ValueError(f"Error fetching data for ticker {ticker}: {str(e)}")


def _get_financials(stock) -> Dict[str, Any]:
    """Extract income statement data."""
    try:
        financials = stock.financials

        if financials.empty:
            return {"error": "No financial data available"}

        # Get the most recent year (first column)
        latest = financials.iloc[:, 0] if not financials.empty else None

        if latest is None:
            return {"error": "No financial data available"}

        return {
            "total_revenue": _safe_get(latest, "Total Revenue"),
            "gross_profit": _safe_get(latest, "Gross Profit"),
            "operating_income": _safe_get(latest, "Operating Income"),
            "net_income": _safe_get(latest, "Net Income"),
            "ebitda": _safe_get(latest, "EBITDA"),
            "period_end": str(financials.columns[0].date()) if len(financials.columns) > 0 else "N/A"
        }
    except Exception as e:
        return {"error": f"Error processing financials: {str(e)}"}


def _get_balance_sheet(stock) -> Dict[str, Any]:
    """Extract balance sheet data."""
    try:
        balance_sheet = stock.balance_sheet

        if balance_sheet.empty:
            return {"error": "No balance sheet data available"}

        # Get the most recent year (first column)
        latest = balance_sheet.iloc[:, 0] if not balance_sheet.empty else None

        if latest is None:
            return {"error": "No balance sheet data available"}

        return {
            "total_assets": _safe_get(latest, "Total Assets"),
            "total_liabilities": _safe_get(latest, "Total Liabilities Net Minority Interest"),
            "stockholder_equity": _safe_get(latest, "Stockholders Equity"),
            "total_debt": _safe_get(latest, "Total Debt"),
            "cash_and_equivalents": _safe_get(latest, "Cash And Cash Equivalents"),
            "current_assets": _safe_get(latest, "Current Assets"),
            "current_liabilities": _safe_get(latest, "Current Liabilities"),
            "period_end": str(balance_sheet.columns[0].date()) if len(balance_sheet.columns) > 0 else "N/A"
        }
    except Exception as e:
        return {"error": f"Error processing balance sheet: {str(e)}"}


def _get_news(stock, limit: int = 3) -> List[Dict[str, str]]:
    """Fetch recent news headlines."""
    try:
        news = stock.news

        if not news:
            return []

        news_items = []
        for item in news[:limit]:
            news_items.append({
                "title": item.get("title", "N/A"),
                "publisher": item.get("publisher", "N/A"),
                "link": item.get("link", ""),
                "published": datetime.fromtimestamp(item.get("providerPublishTime", 0)).strftime("%Y-%m-%d %H:%M") if item.get("providerPublishTime") else "N/A"
            })

        return news_items
    except Exception as e:
        return [{"error": f"Error fetching news: {str(e)}"}]


def _safe_get(series, key: str) -> Any:
    """Safely get value from pandas series."""
    try:
        if key in series.index:
            value = series[key]
            # Convert numpy types to Python types
            if hasattr(value, 'item'):
                return value.item()
            return value
        return "N/A"
    except Exception:
        return "N/A"
