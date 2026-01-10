"""
Utility functions for the Dashboard Analyst service.
"""
from typing import Optional


# ISIN to Ticker mapping for common stocks and ETFs
ISIN_TO_TICKER_MAP = {
    # US Tech Giants
    "US0378331005": "AAPL",      # Apple Inc.
    "US5949181045": "MSFT",      # Microsoft Corporation
    "US88160R1014": "TSLA",      # Tesla Inc.
    "US02079K3059": "GOOGL",     # Alphabet Inc.
    "US0231351067": "AMZN",      # Amazon.com Inc.
    "US30303M1027": "META",      # Meta Platforms Inc.
    "US67066G1040": "NVDA",      # NVIDIA Corporation
    "US4781601046": "JNJ",       # Johnson & Johnson
    "US91324P1021": "UNH",       # UnitedHealth Group

    # Other Major US Stocks
    "US0846707026": "BRK.B",     # Berkshire Hathaway Inc.
    "US1912161007": "KO",        # The Coca-Cola Company
    "US7427181091": "PG",        # Procter & Gamble
    "US9311421039": "WMT",       # Walmart Inc.
    "US17275R1023": "CSCO",      # Cisco Systems
    "US4592001014": "IBM",       # IBM

    # ETFs - World/Global
    "IE00B4L5Y983": "IWDA.AS",   # iShares Core MSCI World UCITS ETF
    "IE00B0M62Q58": "IWDA.L",    # iShares MSCI World (London)
    "IE00BJ0KDQ92": "QDVE.DE",   # Xtrackers MSCI World UCITS ETF
    "LU0274208692": "DBXW.DE",   # Xtrackers MSCI World Swap UCITS ETF

    # ETFs - S&P 500
    "US78462F1030": "SPY",       # SPDR S&P 500 ETF Trust
    "US4642872000": "IVV",       # iShares Core S&P 500 ETF
    "US9229087690": "VOO",       # Vanguard S&P 500 ETF

    # ETFs - NASDAQ
    "US46090E1038": "QQQ",       # Invesco QQQ Trust

    # ETFs - Europe
    "IE00B4K48X80": "ISPA.AS",   # iShares Core EURO STOXX 50 UCITS ETF
    "DE0005933931": "EXS1.DE",   # iShares STOXX Europe 600 UCITS ETF

    # ETFs - Emerging Markets
    "US4642876555": "IEMG",      # iShares Core MSCI Emerging Markets ETF
    "IE00B4L5YC18": "EIMI.AS",   # iShares Core MSCI EM IMI UCITS ETF

    # German DAX Stocks
    "DE0005557508": "DTE.DE",    # Deutsche Telekom AG
    "DE0007164600": "SAP.DE",    # SAP SE
    "DE0005140008": "DBK.DE",    # Deutsche Bank AG
    "DE0007100000": "MBG.DE",    # Mercedes-Benz Group AG
    "DE0005190003": "BMW.DE",    # Bayerische Motoren Werke AG
    "DE0008430026": "MUV2.DE",   # Munich Re
}


def resolve_isin_to_ticker(isin: str) -> Optional[str]:
    """
    Convert an ISIN to a stock ticker symbol.

    Args:
        isin: International Securities Identification Number

    Returns:
        Ticker symbol if found, None otherwise
    """
    # Normalize ISIN (uppercase, strip whitespace)
    isin = isin.strip().upper()

    # Check if ISIN exists in our mapping
    ticker = ISIN_TO_TICKER_MAP.get(isin)

    return ticker


def format_currency(amount: float, currency: str = "USD") -> str:
    """
    Format a number as currency.

    Args:
        amount: The amount to format
        currency: Currency code (USD, EUR, etc.)

    Returns:
        Formatted currency string
    """
    if amount == "N/A" or amount is None:
        return "N/A"

    try:
        amount = float(amount)

        # Format large numbers
        if amount >= 1_000_000_000_000:  # Trillions
            return f"{currency} {amount / 1_000_000_000_000:.2f}T"
        elif amount >= 1_000_000_000:  # Billions
            return f"{currency} {amount / 1_000_000_000:.2f}B"
        elif amount >= 1_000_000:  # Millions
            return f"{currency} {amount / 1_000_000:.2f}M"
        elif amount >= 1_000:  # Thousands
            return f"{currency} {amount / 1_000:.2f}K"
        else:
            return f"{currency} {amount:.2f}"
    except (ValueError, TypeError):
        return "N/A"


def format_percentage(value: float) -> str:
    """
    Format a decimal as percentage.

    Args:
        value: Decimal value (e.g., 0.15 for 15%)

    Returns:
        Formatted percentage string
    """
    if value == "N/A" or value is None:
        return "N/A"

    try:
        value = float(value)
        return f"{value * 100:.2f}%"
    except (ValueError, TypeError):
        return "N/A"


def add_isin_mapping(isin: str, ticker: str) -> None:
    """
    Add a new ISIN to ticker mapping at runtime.

    Args:
        isin: International Securities Identification Number
        ticker: Stock ticker symbol
    """
    ISIN_TO_TICKER_MAP[isin.strip().upper()] = ticker.strip().upper()
