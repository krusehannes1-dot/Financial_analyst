"""
Market Data Service with Technical Analysis
Combines fundamental data with technical indicators for trading decisions.
"""
import yfinance as yf
import pandas as pd
import pandas_ta as ta
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import time
import random

# Configure yfinance to avoid rate limiting
# Set custom headers to mimic browser behavior
import requests
yf.utils.get_json = lambda url, proxy=None, headers=None: requests.get(
    url,
    proxies=proxy,
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://finance.yahoo.com/'
    }
).json()


def get_full_advisor_data(ticker: str) -> Dict[str, Any]:
    """
    Fetch comprehensive market data including technical indicators and Wall Street consensus.

    This function is the mathematical foundation for AI-driven trading decisions.
    It combines:
    - Historical price data (1 year)
    - Technical indicators (RSI, SMA, Support/Resistance)
    - Wall Street analyst consensus
    - Fundamental valuation metrics

    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'NVDA')

    Returns:
        Dictionary containing all calculated metrics and indicators
    """
    try:
        # Add small random delay to avoid rate limiting
        time.sleep(random.uniform(0.5, 1.5))

        stock = yf.Ticker(ticker)

        # Get basic info first
        info = stock.info

        # Fetch 1 year of historical data
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        hist = stock.history(start=start_date, end=end_date)

        if hist.empty:
            raise ValueError(f"No historical data available for {ticker}")

        # ============================================================
        # TECHNICAL ANALYSIS - The Algorithmic Foundation
        # ============================================================

        # Calculate RSI (Relative Strength Index) - Momentum indicator
        hist['RSI'] = ta.rsi(hist['Close'], length=14)

        # Calculate Moving Averages - Trend identification
        hist['SMA_50'] = ta.sma(hist['Close'], length=50)
        hist['SMA_200'] = ta.sma(hist['Close'], length=200)

        # Get most recent values (drop NaN)
        current_rsi = hist['RSI'].dropna().iloc[-1] if not hist['RSI'].dropna().empty else None
        current_sma_50 = hist['SMA_50'].dropna().iloc[-1] if not hist['SMA_50'].dropna().empty else None
        current_sma_200 = hist['SMA_200'].dropna().iloc[-1] if not hist['SMA_200'].dropna().empty else None

        # Calculate MACD (Moving Average Convergence Divergence)
        macd = ta.macd(hist['Close'])
        if macd is not None and not macd.empty:
            current_macd = macd['MACD_12_26_9'].iloc[-1] if 'MACD_12_26_9' in macd.columns else None
            current_macd_signal = macd['MACDs_12_26_9'].iloc[-1] if 'MACDs_12_26_9' in macd.columns else None
            current_macd_histogram = macd['MACDh_12_26_9'].iloc[-1] if 'MACDh_12_26_9' in macd.columns else None
        else:
            current_macd = None
            current_macd_signal = None
            current_macd_histogram = None

        # ============================================================
        # SUPPORT & RESISTANCE LEVELS - Critical Price Zones
        # ============================================================

        # Use last 90 days for S/R calculation
        recent_90d = hist.tail(90)

        support_level = float(recent_90d['Low'].min())
        resistance_level = float(recent_90d['High'].max())

        # Calculate additional support/resistance using pivot points
        recent_high = float(recent_90d['High'].max())
        recent_low = float(recent_90d['Low'].min())
        recent_close = float(hist['Close'].iloc[-1])

        # Pivot Point (Standard)
        pivot_point = (recent_high + recent_low + recent_close) / 3
        resistance_1 = (2 * pivot_point) - recent_low
        support_1 = (2 * pivot_point) - recent_high

        # ============================================================
        # CURRENT PRICE & VOLUME ANALYSIS
        # ============================================================

        current_price = float(hist['Close'].iloc[-1])
        avg_volume_30d = float(hist['Volume'].tail(30).mean())
        current_volume = float(hist['Volume'].iloc[-1])
        volume_ratio = current_volume / avg_volume_30d if avg_volume_30d > 0 else 1.0

        # Price change metrics
        price_change_1d = ((current_price - float(hist['Close'].iloc[-2])) / float(hist['Close'].iloc[-2])) * 100
        price_change_5d = ((current_price - float(hist['Close'].iloc[-6])) / float(hist['Close'].iloc[-6])) * 100 if len(hist) >= 6 else 0
        price_change_1m = ((current_price - float(hist['Close'].iloc[-22])) / float(hist['Close'].iloc[-22])) * 100 if len(hist) >= 22 else 0

        # ============================================================
        # VOLATILITY METRICS
        # ============================================================

        # Calculate Bollinger Bands
        bb = ta.bbands(hist['Close'], length=20, std=2)
        if bb is not None and not bb.empty:
            bb_upper = bb['BBU_20_2.0'].iloc[-1] if 'BBU_20_2.0' in bb.columns else None
            bb_middle = bb['BBM_20_2.0'].iloc[-1] if 'BBM_20_2.0' in bb.columns else None
            bb_lower = bb['BBL_20_2.0'].iloc[-1] if 'BBL_20_2.0' in bb.columns else None
        else:
            bb_upper = None
            bb_middle = None
            bb_lower = None

        # Average True Range (Volatility measure)
        atr = ta.atr(hist['High'], hist['Low'], hist['Close'], length=14)
        current_atr = atr.iloc[-1] if atr is not None and not atr.empty else None

        # ============================================================
        # WALL STREET CONSENSUS - Analyst Opinions
        # ============================================================

        target_mean_price = info.get('targetMeanPrice')
        target_high_price = info.get('targetHighPrice')
        target_low_price = info.get('targetLowPrice')
        recommendation_key = info.get('recommendationKey', 'none')
        number_of_analyst_opinions = info.get('numberOfAnalystOpinions', 0)

        # Calculate upside potential
        upside_potential = None
        if target_mean_price and current_price > 0:
            upside_potential = ((target_mean_price - current_price) / current_price) * 100

        # ============================================================
        # FUNDAMENTAL METRICS - Valuation
        # ============================================================

        forward_pe = info.get('forwardPE')
        trailing_pe = info.get('trailingPE')
        peg_ratio = info.get('pegRatio')
        debt_to_equity = info.get('debtToEquity')
        price_to_book = info.get('priceToBook')
        profit_margins = info.get('profitMargins')
        revenue_growth = info.get('revenueGrowth')
        earnings_growth = info.get('earningsGrowth')

        # Market Cap & Beta
        market_cap = info.get('marketCap')
        beta = info.get('beta')

        # ============================================================
        # TREND ANALYSIS - Determine Market Regime
        # ============================================================

        trend = "NEUTRAL"
        if current_sma_50 and current_sma_200:
            if current_sma_50 > current_sma_200 and current_price > current_sma_50:
                trend = "STRONG_UPTREND"
            elif current_sma_50 > current_sma_200:
                trend = "UPTREND"
            elif current_sma_50 < current_sma_200 and current_price < current_sma_50:
                trend = "STRONG_DOWNTREND"
            elif current_sma_50 < current_sma_200:
                trend = "DOWNTREND"

        # ============================================================
        # COMPILE COMPREHENSIVE ADVISOR DATA
        # ============================================================

        return {
            # Basic Info
            "ticker": ticker,
            "name": info.get('longName', ticker),
            "sector": info.get('sector', 'N/A'),
            "industry": info.get('industry', 'N/A'),
            "currency": info.get('currency', 'USD'),

            # Current Price & Volume
            "current_price": current_price,
            "avg_volume_30d": avg_volume_30d,
            "current_volume": current_volume,
            "volume_ratio": volume_ratio,

            # Price Changes
            "price_change_1d": price_change_1d,
            "price_change_5d": price_change_5d,
            "price_change_1m": price_change_1m,

            # Technical Indicators
            "rsi": current_rsi,
            "sma_50": current_sma_50,
            "sma_200": current_sma_200,
            "macd": current_macd,
            "macd_signal": current_macd_signal,
            "macd_histogram": current_macd_histogram,

            # Bollinger Bands
            "bb_upper": bb_upper,
            "bb_middle": bb_middle,
            "bb_lower": bb_lower,

            # Volatility
            "atr": current_atr,

            # Support & Resistance
            "support_level": support_level,
            "resistance_level": resistance_level,
            "pivot_point": pivot_point,
            "support_1": support_1,
            "resistance_1": resistance_1,

            # Trend Analysis
            "trend": trend,

            # Wall Street Consensus
            "target_mean_price": target_mean_price,
            "target_high_price": target_high_price,
            "target_low_price": target_low_price,
            "recommendation_key": recommendation_key,
            "number_of_analysts": number_of_analyst_opinions,
            "upside_potential": upside_potential,

            # Fundamental Metrics
            "forward_pe": forward_pe,
            "trailing_pe": trailing_pe,
            "peg_ratio": peg_ratio,
            "debt_to_equity": debt_to_equity,
            "price_to_book": price_to_book,
            "profit_margins": profit_margins,
            "revenue_growth": revenue_growth,
            "earnings_growth": earnings_growth,
            "market_cap": market_cap,
            "beta": beta,

            # Metadata
            "data_timestamp": datetime.now().isoformat(),
            "historical_days": len(hist)
        }

    except Exception as e:
        raise ValueError(f"Error fetching advisor data for {ticker}: {str(e)}")


def format_advisor_data_summary(data: Dict[str, Any]) -> str:
    """
    Format advisor data into a human-readable summary for LLM consumption.

    Args:
        data: Dictionary from get_full_advisor_data()

    Returns:
        Formatted string summary
    """
    summary = f"""
=== MARKET DATA SUMMARY ===
Company: {data['name']} ({data['ticker']})
Sector: {data['sector']} | Industry: {data['industry']}

CURRENT MARKET STATUS:
- Price: {data['current_price']:.2f} {data['currency']}
- 1-Day Change: {data['price_change_1d']:.2f}%
- 5-Day Change: {data['price_change_5d']:.2f}%
- 1-Month Change: {data['price_change_1m']:.2f}%
- Volume Ratio: {data['volume_ratio']:.2f}x (vs 30-day avg)

TECHNICAL INDICATORS:
- RSI(14): {data['rsi']:.2f if data['rsi'] else 'N/A'} {'[OVERBOUGHT]' if data['rsi'] and data['rsi'] > 70 else '[OVERSOLD]' if data['rsi'] and data['rsi'] < 30 else ''}
- Trend: {data['trend']}
- SMA50: {data['sma_50']:.2f if data['sma_50'] else 'N/A'}
- SMA200: {data['sma_200']:.2f if data['sma_200'] else 'N/A'}
- MACD: {data['macd']:.2f if data['macd'] else 'N/A'}

SUPPORT & RESISTANCE:
- Support (90d): {data['support_level']:.2f}
- Resistance (90d): {data['resistance_level']:.2f}
- Pivot Point: {data['pivot_point']:.2f}

WALL STREET CONSENSUS:
- Recommendation: {data['recommendation_key'].upper()}
- Target Price: {data['target_mean_price']:.2f if data['target_mean_price'] else 'N/A'}
- Upside Potential: {data['upside_potential']:.2f if data['upside_potential'] else 'N/A'}%
- Analysts: {data['number_of_analysts']}

VALUATION METRICS:
- Forward P/E: {data['forward_pe']:.2f if data['forward_pe'] else 'N/A'}
- PEG Ratio: {data['peg_ratio']:.2f if data['peg_ratio'] else 'N/A'}
- Debt/Equity: {data['debt_to_equity']:.2f if data['debt_to_equity'] else 'N/A'}
"""
    return summary
