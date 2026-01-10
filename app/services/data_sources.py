"""
Multi-Source Data Provider
Provides fallback mechanism when primary data source fails.
"""
import yfinance as yf
import requests
import time
import random
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class DataSourceError(Exception):
    """Raised when a data source fails."""
    pass


class YFinanceSource:
    """Yahoo Finance data source with anti-blocking measures."""

    def __init__(self):
        self.name = "Yahoo Finance"
        self._configure_headers()

    def _configure_headers(self):
        """Configure yfinance with browser-like headers."""
        yf.utils.get_json = lambda url, proxy=None, headers=None: requests.get(
            url,
            proxies=proxy,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': 'https://finance.yahoo.com/'
            },
            timeout=10
        ).json()

    def fetch_quote(self, ticker: str) -> Dict[str, Any]:
        """Fetch current quote data."""
        try:
            # Random delay to avoid rate limiting
            time.sleep(random.uniform(1, 2))

            stock = yf.Ticker(ticker)
            info = stock.info

            if not info or 'currentPrice' not in info:
                raise DataSourceError(f"No data returned for {ticker}")

            return info

        except Exception as e:
            logger.error(f"YFinance error for {ticker}: {str(e)}")
            raise DataSourceError(f"YFinance failed: {str(e)}")

    def fetch_history(self, ticker: str, period: str = "1y") -> Any:
        """Fetch historical price data."""
        try:
            time.sleep(random.uniform(1, 2))

            stock = yf.Ticker(ticker)
            hist = stock.history(period=period)

            if hist.empty:
                raise DataSourceError(f"No historical data for {ticker}")

            return hist

        except Exception as e:
            logger.error(f"YFinance history error for {ticker}: {str(e)}")
            raise DataSourceError(f"YFinance history failed: {str(e)}")


class AlphaVantageSource:
    """Alpha Vantage data source (requires API key)."""

    def __init__(self, api_key: Optional[str] = None):
        import os
        self.name = "Alpha Vantage"
        self.api_key = api_key or os.getenv("ALPHA_VANTAGE_API_KEY")
        self.base_url = "https://www.alphavantage.co/query"

    def fetch_quote(self, ticker: str) -> Dict[str, Any]:
        """Fetch current quote from Alpha Vantage."""
        if not self.api_key:
            raise DataSourceError("Alpha Vantage API key not configured")

        try:
            params = {
                'function': 'GLOBAL_QUOTE',
                'symbol': ticker,
                'apikey': self.api_key
            }

            response = requests.get(self.base_url, params=params, timeout=10)
            data = response.json()

            if 'Global Quote' not in data:
                raise DataSourceError("Invalid response from Alpha Vantage")

            quote = data['Global Quote']

            # Convert to yfinance-like format
            return {
                'currentPrice': float(quote.get('05. price', 0)),
                'previousClose': float(quote.get('08. previous close', 0)),
                'open': float(quote.get('02. open', 0)),
                'dayHigh': float(quote.get('03. high', 0)),
                'dayLow': float(quote.get('04. low', 0)),
                'volume': int(quote.get('06. volume', 0)),
                'symbol': quote.get('01. symbol', ticker)
            }

        except Exception as e:
            logger.error(f"Alpha Vantage error for {ticker}: {str(e)}")
            raise DataSourceError(f"Alpha Vantage failed: {str(e)}")


class PolygonSource:
    """Polygon.io data source (requires API key)."""

    def __init__(self, api_key: Optional[str] = None):
        import os
        self.name = "Polygon.io"
        self.api_key = api_key or os.getenv("POLYGON_API_KEY")
        self.base_url = "https://api.polygon.io"

    def fetch_quote(self, ticker: str) -> Dict[str, Any]:
        """Fetch current quote from Polygon."""
        if not self.api_key:
            raise DataSourceError("Polygon API key not configured")

        try:
            # Get previous close
            url = f"{self.base_url}/v2/aggs/ticker/{ticker}/prev"
            params = {'apiKey': self.api_key}

            response = requests.get(url, params=params, timeout=10)
            data = response.json()

            if data.get('status') != 'OK' or not data.get('results'):
                raise DataSourceError("Invalid response from Polygon")

            result = data['results'][0]

            return {
                'currentPrice': result.get('c', 0),  # close
                'open': result.get('o', 0),
                'dayHigh': result.get('h', 0),
                'dayLow': result.get('l', 0),
                'volume': result.get('v', 0),
                'symbol': ticker
            }

        except Exception as e:
            logger.error(f"Polygon error for {ticker}: {str(e)}")
            raise DataSourceError(f"Polygon failed: {str(e)}")


class MarketDataProvider:
    """
    Multi-source data provider with automatic fallback.

    Tries data sources in order until one succeeds:
    1. Yahoo Finance (primary, free)
    2. Alpha Vantage (fallback, requires key)
    3. Polygon.io (fallback, requires key)
    """

    def __init__(self):
        self.sources = []

        # Always try Yahoo Finance first (free)
        self.sources.append(YFinanceSource())

        # Add Alpha Vantage if API key is available
        import os
        if os.getenv("ALPHA_VANTAGE_API_KEY"):
            self.sources.append(AlphaVantageSource())
            logger.info("Alpha Vantage source enabled")

        # Add Polygon if API key is available
        if os.getenv("POLYGON_API_KEY"):
            self.sources.append(PolygonSource())
            logger.info("Polygon source enabled")

        logger.info(f"Initialized with {len(self.sources)} data source(s)")

    def get_quote(self, ticker: str) -> Dict[str, Any]:
        """
        Fetch quote data with automatic fallback.

        Args:
            ticker: Stock ticker symbol

        Returns:
            Quote data dictionary

        Raises:
            DataSourceError: If all sources fail
        """
        last_error = None

        for source in self.sources:
            try:
                logger.info(f"Trying {source.name} for {ticker}")
                data = source.fetch_quote(ticker)
                logger.info(f"✓ {source.name} succeeded for {ticker}")
                return data

            except DataSourceError as e:
                logger.warning(f"✗ {source.name} failed for {ticker}: {str(e)}")
                last_error = e
                continue

        # All sources failed
        error_msg = f"All data sources failed for {ticker}"
        if last_error:
            error_msg += f". Last error: {str(last_error)}"

        raise DataSourceError(error_msg)

    def get_history(self, ticker: str, period: str = "1y") -> Any:
        """
        Fetch historical data (only supports Yahoo Finance for now).

        Args:
            ticker: Stock ticker symbol
            period: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)

        Returns:
            Pandas DataFrame with historical data

        Raises:
            DataSourceError: If fetch fails
        """
        # For now, only YFinance supports historical data easily
        source = YFinanceSource()

        try:
            logger.info(f"Fetching history from {source.name} for {ticker}")
            hist = source.fetch_history(ticker, period)
            logger.info(f"✓ {source.name} history succeeded for {ticker}")
            return hist

        except DataSourceError as e:
            logger.error(f"Failed to fetch history for {ticker}: {str(e)}")
            raise


# Global instance
_provider = None


def get_market_data_provider() -> MarketDataProvider:
    """Get or create the global MarketDataProvider instance."""
    global _provider
    if _provider is None:
        _provider = MarketDataProvider()
    return _provider
